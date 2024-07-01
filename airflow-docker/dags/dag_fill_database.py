import requests

import datetime as dt

from airflow.models import DAG
from airflow.operators.python import PythonOperator


from db_utils import is_record, add_row
from utils import make_time_range

from cred_airflow import API_KEY
from settings import db_names, db_to_stock


def get_data(symbol: str, date: str) -> bool:

    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&month={date}&outputsize=full&apikey={API_KEY.get_key()}"
    respocne = requests.get(url).json()
    try:
        respocne_json = respocne["Time Series (5min)"]
        # print("All done")
    except Exception as e:
        print("something was wrong, API ", API_KEY.get_key())
        API_KEY.next_key()
        print(f"new key {API_KEY.get_key()}")

        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&month={date}&outputsize=full&apikey={API_KEY.get_key()}"
        respocne = requests.get(url).json()
        try:
            respocne_json = respocne["Time Series (5min)"]
        except:
            print(respocne)
            print(e)
            return False

    result = []
    for key, value in respocne_json.items():

        data = [key]
        data.extend(list(value.values()))
        result.append(data)

    try:
        for row in result:
            add_row(row, symbol)
        return True
    except Exception as e:
        print(f"Error in add values for {symbol} to DB : {e}")
        return False


def start():

    symbols = []

    for name in db_names:
        if not is_record(name):
            symbols.append(db_to_stock[name])

    if len(symbols) != 0:
        print(f"empty databases: {symbols}")
        dates = make_time_range("2023-06", "2024-06")
        for symbol in symbols:
            for date in dates:
                if not get_data(symbol, date):
                    break
                else:
                    print(f"{symbol} for {date} was handled")


args = {
    "owner": "airflow",  # Информация о владельце DAG
    "start_date": dt.datetime.now(),  # Время начала выполнения пайплайна
    "retries": 1,  # Количество повторений в случае неудач
    "retry_delay": dt.timedelta(days=1),  # Пауза между повторами
    "depends_on_past": False,  # Зависимость от успешного окончания предыдущего запуска
}

with DAG(dag_id="dag_fill_db", schedule_interval="@daily", default_args=args) as dag:

    fill_db = PythonOperator(task_id="fill_db", python_callable=start, dag=dag)

    fill_db
