import datetime as dt
import pandas as pd
import numpy as np

from airflow import DAG
from airflow.operators.python import PythonOperator

from db_utils import (
    create_engine,
    create_session,
    create_cursor,
    add_row_to_all,
    delete_from_table,
)
from cred_airflow import DB_URL
from settings import db_names


def compare():
    delete_from_table("all_data")
    df = pd.DataFrame(
        columns=[
            "date",
            "stock_name",
            "open",
            "high",
            "low",
            "close",
            "ma",
            "rsi",
            "macd",
            "signal",
        ]
    )
    for db in db_names:
        print(f"start for {db}")
        query = f"""
select  t1.date, t1.open, t1.high, t1.low, t1.close, t2.close as ma, t3.rsi, t4.macd, t4.signal from  public.{db} as t1
inner join public.{db} as t2
ON t1.date = t2.date
inner join public.{db}_rsi as t3
on t1.date = t3.date
inner join public.{db}_macd as t4
on t1.date = t4.date
"""

        # db_session = create_session()
        # conn = db_session.connection()

        table = create_cursor().execute(query)

        get_df = pd.DataFrame(
            table,
            columns=[
                "date",
                "open",
                "high",
                "low",
                "close",
                "ma",
                "rsi",
                "macd",
                "signal",
            ],
        )
        stock_name = pd.Series(np.full(get_df.shape[0], db))
        get_df = get_df.insert(1, "stock_name", stock_name)
        df = pd.concat([df, get_df])
    engine = create_engine(DB_URL)
    df.to_sql("all_data", engine, if_exists="replace")
    # db_session.close()
    # for row in table:
    #     add_row_to_all(db, row)
    # print(list(table)[:10])


args = {
    "owner": "airflow",  # Информация о владельце DAG
    "start_date": dt.datetime.now(),  # Время начала выполнения пайплайна
    "retries": 1,  # Количество повторений в случае неудач
    "retry_delay": dt.timedelta(days=1),  # Пауза между повторами
    "depends_on_past": False,  # Зависимость от успешного окончания предыдущего запуска
}

with DAG(dag_id="dag_concater", schedule_interval="@daily", default_args=args) as dag:

    compare = PythonOperator(task_id="start_compare", python_callable=compare, dag=dag)

    compare
