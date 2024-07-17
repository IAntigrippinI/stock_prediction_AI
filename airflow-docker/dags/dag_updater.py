import datetime
import requests

import datetime as dt
import pandas as pd
import numpy as np

from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

from db_utils import add_row, is_record, get_last_date

from cred_airflow import API_KEY
from settings import stock_names, db_names, db_to_stock


def get_today():
    month, year = str(datetime.datetime.utcnow().month), str(
        datetime.datetime.utcnow().year
    )

    return year + "-" + "0" * (2 - len(month)) + month


def get_data(symbol):
    print(get_today())
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={db_to_stock[symbol]}&interval=5min&month={get_today()}&outputsize=full&apikey={API_KEY.get_key()}"
    respocne = requests.get(url).json()
    try:
        respocne_json = respocne["Time Series (5min)"]
    except Exception as e:

        print(respocne)
        return "0"
    # print(respocne)

    result = []
    for key, value in respocne_json.items():
        data = [key]
        data.extend(list(value.values()))
        result.append(data)
    result = np.array(result)
    return result


def find_new_data(data: np.array, last_date: str):
    dataes = data[:, 0].astype(str)
    new_records = dataes > last_date
    return new_records


def find_new():

    for symbol in db_names:
        if not is_record(symbol):
            continue

        data = get_data(symbol)
        df = pd.DataFrame(
            data, columns=["date", "open", "high", "low", "close", "volume"]
        )
        last_date = get_last_date(symbol)
        df_new = df[df.date > last_date]
        if df_new.shape[0] != 0:
            print(f"add new data for {symbol}")
            print(df_new)
            df_new.apply(lambda x: add_row(x, symbol), axis=1)
        else:
            print(f"New data for {symbol} was not found")


args = {
    "owner": "airflow",  # Информация о владельце DAG
    "start_date": dt.datetime(2024, 6, 25),  # Время начала выполнения пайплайна
    "retries": 1,  # Количество повторений в случае неудач
    "retry_delay": dt.timedelta(minutes=1),  # Пауза между повторами
    "depends_on_past": False,  # Зависимость от успешного окончания предыдущего запуска
}


with DAG(
    dag_id="dag_updater",  # Имя DAG
    schedule_interval="@daily",  # Периодичность запуска
    default_args=args,  # Базовые аргументы
) as dag:

    # BashOperator, выполняющий указанную bash-команду
    first_task = BashOperator(
        task_id="first_task",
        bash_command='echo "GOOOOO"',
        dag=dag,
    )

    start = PythonOperator(task_id="pasrecompaire", python_callable=find_new, dag=dag)

    first_task >> start
