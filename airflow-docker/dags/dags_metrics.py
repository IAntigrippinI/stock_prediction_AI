import datetime as dt


from airflow.models import DAG
from airflow.operators.python import PythonOperator

from fun_for_metrics import start_calc_metrics

from settings import db_names


def start():
    start_calc_metrics()


args = {
    "owner": "airflow",
    "start_date": dt.datetime(2024, 6, 25),
    "retries": 1,
    "retry_delay": dt.timedelta(minutes=1),
    "depends_on_past": False,
}


with DAG(
    dag_id="dag_metrics",
    schedule_interval="@daily",
    default_args=args,
) as dag:

    start = PythonOperator(task_id="pasrecompaire", python_callable=start, dag=dag)

    start
