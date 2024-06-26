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
from class_API import API

API_KEY = API(["YOUR_API_KEY1", "YOUR_API_KEY2", и тд])
DB_URL = "postgresql+psycopg2://airflow:airflow@postgres/<DataBaseName>"

```
# Примечания
* 1. Перед запуском необходимо создать базы данных с именами, в соответствии с именами, заданными в settings.py -> db_names:
    * 1.1 Базы данных для хранения информации должны содержать столбы: (date(timestamp), open(float), high(float), low(float), close(float), volume(float))
    * 1.2 Базы данных для хранения информации должны содержать столбы: (date(timestamp), open(float), high(float), low(float), close(float)), а также называться в соответствии с предсказываемой компанией (напр. AAPL_predict)
    * 1.3 При изменении списка отслеживаемых акций, следует создать классы на пободии предоставленных в models_sql.py 
# Описание вспомогательных файлов
* 1. **class_API**- представляет собой класс, содержащий список API ключей для доступа к API [Aplhavantage](https://www.alphavantage.co/). Ввиду того, что сервис предоставляет 25 запросов в сутки для стандартной подписки, заполнение базы данных за один раз становится невозможным. Решить данную проблему помог данный класс: При обнаружении факта превышения лимита запросов, использую данный класс и его метод, можно получить следующий API ключ из списка, если такой есть
* 2. **db_utils** - содержит функции для работы с базой данных
* 3. **fun_for_predict** - содержит функции, необходимые для предсказания стоимости акций

# Настраиваемые параметры
### Настраиваемые параметры находятся в settings.py
### Описание параметров:
* 1. **db_names** - список названий баз данных (**ВАЖНО** : при замене значений следует создать новые классы на пободии классов, находящихся в model_sql.py)
* 2. **dt_to_stock** - словарь для определения связи между названиями баз данных и названиями акций
* 3. **stock_names** - список названий акций
* 4. **PREDICT_TIME** - количество 5-тии минутных отрезков для предсказания (напр. при PREDICT_TIME = 100 будет получены прогнозы для следующих 500 минут) 
* 5. **N_DAYS_BEFORE_FOR_MODEL** - количество 5-ти минутных отрезков ранее последней даты, на которые будет опираться модель при прогнозировании. Также задает кол-во фичей для модели (напр. для N_DAYS_BEFORE_FOR_MODEL = 100 кол-во признаков = 400, т.к. каждый 5-ти минутный отрезок имеет 4 признака). В соответствии с этим, можно использовать модели, обученные для предсказаний на основе данных более поздних временных отрезков. **Модели должны иметь название: model_{name_db}_{target}.pkl**
