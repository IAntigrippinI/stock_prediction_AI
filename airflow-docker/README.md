# Запуск

### 1. Создание папок plugins, config, logs
```
mkdir -p ./logs ./plugins ./config
```

### 2. Создание .env
```
echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env
```
### 3. Инициализация базы данных
```
docker compose up airflow-init
```
### 4. Запуск 
```
docker compose up
```

### 5. Создание файла cred_airflow.py, внутри:
```
API_KEY = "<YOUR_API_KEY>"
DB_URL = "postgresql+psycopg2://airflow:airflow@postgres/<YOUR_DB>"
```
### Примечания