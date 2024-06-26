import sqlalchemy
import requests
import json

import pandas as pd

from db_utils import create_session
from models_sql import ibm
from utils import make_time_range

from cred import API_KEY


def add_row(row):
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
    
    

def get_data(date):
    #url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&month={date}&apikey={API_KEY}'
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&month={date}&outputsize=full&apikey={API_KEY}'
    respocne = requests.get(url).json()
    try:
        respocne_json = respocne['Time Series (5min)']
    except Exception as e:

        print(respocne)
        return '0'
    #print(respocne)
    with open('res.json', 'w') as f:
        json.dump(respocne_json, f, ensure_ascii=True, indent=4)
    result = []
    for key,value in respocne_json.items():
        #print(f'{key}, {list(value.values())}')
        data = [key]
        data.extend(list(value.values()))
        result.append(data)
    #print(result)
    for row in result:
        add_row(row)


    
    
def start():
    dates = make_time_range('2023-06', '2024-06')
    for date in dates:
        get_data(date)

def main():
    start()

if __name__ == "__main__":
    main()