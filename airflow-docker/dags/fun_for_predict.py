import joblib

import pandas as pd
import numpy as np

from datetime import datetime, timedelta

from db_utils import create_cursor

from settings import PREDICT_TIME, N_DAYS_BEFORE_FOR_MODEL

import warnings

warnings.filterwarnings("ignore")


def create_columns() -> list:
    time_before_for_predict = 1000
    new_columns = ["date"]
    columns = ["open", "high", "low", "close"]
    time_before_for_predict = 3
    for i in range(time_before_for_predict, 0, -1):
        for col in columns:
            new_columns.append(col + "_" + str(i) + "b")
    return new_columns


def make_date_range(start: str):
    start_date = datetime.strptime(str(start), "%Y-%m-%d %H:%M:%S")
    date_range = []

    date_now = start_date
    for i in range(PREDICT_TIME):
        date_now += timedelta(minutes=5)
        date_range.append(date_now)
    return date_range


def convert_to_one_row(row: list) -> list:

    result_row = []

    for i in range(N_DAYS_BEFORE_FOR_MODEL - 1, -1, -1):
        for j in range(1, len(row[i])):
            result_row.append(row[i][j])

    return result_row


def pred(row, symbol, target):
    model = joblib.load(f"/opt/airflow/dags/models/model_{symbol}_{target}.pkl")
    pred = model.predict(np.array(row).reshape(1, -1))
    return pred[0]


def start_predict(row, symbol):
    results = []

    for i in range(PREDICT_TIME):

        row.append(pred(row, symbol, "open"))

        row.append(pred(row, symbol, "high"))

        row.append(pred(row, symbol, "low"))

        row.append(pred(row, symbol, "close"))

        results.append(row[-4:])

        row = row[4:]

    return results


def get_predict_data(symbol):
    last_row = list(
        create_cursor().execute(
            f"SELECT date,open,high,low,close FROM public.{symbol} order by date DESC limit {PREDICT_TIME}"
        )
    )

    row = convert_to_one_row(last_row)

    dates = np.array(make_date_range(last_row[0][0]))

    result_predicts = start_predict(row, symbol)
    df = pd.DataFrame(result_predicts)
    df.insert(0, "date", dates)
    # print(df.head(10))
    df.columns = ["date", "open", "high", "low", "close"]

    return df
