import datetime
import requests

import datetime as dt
import pandas as pd
import numpy as np

from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base


API_KEY = "YOUR API-KEY"
DB_URL = "YOUR URL FOR DB CONNECT"

DeclBase = declarative_base()


class ibm(DeclBase):
    __tablename__ = "ibm"
    date = Column(DateTime, default=datetime.datetime.utcnow, primary_key=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float)


def add_row(row: pd.Series):
    try:
        row = row.tolist()
        print(row)
        db_session = create_session()
        new_row = ibm()
        new_row.date = row[0]
        new_row.open = row[1]
        new_row.high = row[2]
        new_row.low = row[3]
        new_row.close = row[4]
        new_row.volume = row[5]
        db_session.add(new_row)
        db_session.commit()
    except:
        pass


def get_today():
    month, year = str(datetime.datetime.utcnow().month), str(
        datetime.datetime.utcnow().year
    )

    return year + "-" + "0" * (2 - len(month)) + month


def get_data():
    print(get_today())
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&month={get_today()}&outputsize=full&apikey={API_KEY}"
    respocne = requests.get(url).json()
    try:
        respocne_json = respocne["Time Series (5min)"]
    except Exception as e:

        print(respocne)
        return "0"
    # print(respocne)

    result = []
    for key, value in respocne_json.items():
        # print(f'{key}, {list(value.values())}')
        data = [key]
        data.extend(list(value.values()))
        result.append(data)
    result = np.array(result)
    return result


def create_session():
    engine = create_engine(DB_URL)
    SessionClass = sessionmaker(bind=engine)
    return SessionClass()


def get_last_date() -> str:
    db_session = create_session()
    last_date = db_session.query(ibm).order_by(desc(ibm.date)).first().date
    return str(last_date)


def find_new_data(data: np.array, last_date: str):
    dataes = data[:, 0].astype(str)
    new_records = dataes > last_date
    return


def find_new():
    data = get_data()
    df = pd.DataFrame(data, columns=["date", "open", "high", "low", "close", "volume"])
    last_date = get_last_date()
    df_new = df[df.date > last_date]
    df.apply(lambda x: add_row(x), axis=1)
    # df_new.to_csv("output.csv")

    # res = find_new_data(data, get_last_date())
    # print(res)


def add_to_db():
    df = pd.read_csv("output.csv", index_col=0)
    print(df)
    df.apply(lambda x: add_row(x), axis=1)


args = {
    "owner": "airflow",  # Информация о владельце DAG
    "start_date": dt.datetime(2024, 6, 25),  # Время начала выполнения пайплайна
    "retries": 1,  # Количество повторений в случае неудач
    "retry_delay": dt.timedelta(minutes=1),  # Пауза между повторами
    "depends_on_past": False,  # Зависимость от успешного окончания предыдущего запуска
}


with DAG(
    dag_id="update_dag",  # Имя DAG
    schedule_interval="10 * * * *",  # Периодичность запуска
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
