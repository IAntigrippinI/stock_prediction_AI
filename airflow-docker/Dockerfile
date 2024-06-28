FROM apache/airflow:2.9.1
COPY requirements_airflow.txt requirements_airflow.txt
USER root
RUN apt-get update
RUN apt-get install -y libpq-dev gcc
USER airflow 
RUN pip install -r requirements_airflow.txt
