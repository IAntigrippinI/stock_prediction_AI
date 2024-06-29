# stock_prediction_AI

# **Запуск в docker см. в airflow-docker**

## Как начать

### 1. Запустить образ PostrgreSQL: 
```linux
docker run --name database -p 5432:5432 -e POSTGRES_PASSWORD=your_password -d postgres
```   


### 2. Активировать виртуальное оружение и устанвоить зависимости
```
python3 -m venv venv
source venv/bin/activate (for windows: ./venv/Scripts/activate)
pip install -r requirements.txt
```


### 3. Перейти в директорию для создания бд
```
cd backend
``` 

### 4. Создать файл cred.py и добавить в него URL для подключения к бд и API-KEY
```python
API_KEY = 'YOUR_API_KEY'
DB_URL = "postgresql://usernameDB:password@localhost/postgres"
```

### 5. Запустить скрипт для заполнения бд
```
python3 backend.py
```

## Запуск apache-airflow для постоянного обновления базы
### 1. Открыть новый терминал. Перейти в папку airflow-proj и создать в нем виртуальное окружение, а также установить зависимости
```
cd airflow-proj
python3 -m venv airflow-env
source airflow-env/bin/activate
pip install -r requirements_airflow.txt
```

### 2. Добавить в папку airflow-proj/venv/lib/airflow/example_dags файл update_dag.py