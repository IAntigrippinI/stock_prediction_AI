import sqlalchemy
import requests
import json

import pandas as pd

from cred import API_KEY

def get_values(row) -> tuple:
    print(row + '\n\n')

def get_data():
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&month=2023-06&apikey={API_KEY}'
    respocne = requests.get(url).json()['Time Series (5min)']
    #print(respocne)
    with open('res.json', 'w') as f:
        json.dump(respocne, f, ensure_ascii=True, indent=4)
    result = []
    for key,value in respocne.items():
        print(f'{key}, {list(value.values())}')
        data = [key]
        data.extend(list(value.values()))
        result.append(data)
    print(result)
    df = pd.DataFrame(result, columns=['Time', 'open', 'high', 'low', 'close', 'volume'])
    df.to_csv('data/result.csv', index=False)

    
    


def main():
    get_data()

if __name__ == "__main__":
    main()