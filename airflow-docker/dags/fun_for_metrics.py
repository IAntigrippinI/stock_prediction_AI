import numpy as np
import pandas as pd

from db_utils import (
    get_table_for_metrics,
    add_row_metric,
    delete_from_table,
    add_row_macd,
)

import warnings

warnings.filterwarnings("ignore")

PERIOD = 12


def calculate_ma(df, symbol):
    # delete_from_table(f"{symbol}_ma")
    try:
        print(f"start fidd {symbol}_ma")
        result_df = pd.DataFrame(columns=["date", "ma"])
        for i in range(0, df.shape[0], PERIOD):
            # print(i)
            if (i + i + PERIOD) // 2 > df.shape[0]:
                date = df.date[df.shape[0] - 1]
            else:
                date = df.date[(i + i + PERIOD) // 2]
            result_df.loc[result_df.shape[0]] = [
                date,
                df.close[i : i + PERIOD].mean(),
            ]
        # print(result_df)
        result_df.apply(lambda x: add_row_metric(x, symbol, "ma"), axis=1)
        print(f"finish fidd {symbol}_ma")
    except Exception as e:
        print(f"in calculate_ma : {e}")


def calculate_rsi(df: pd.DataFrame, symbol):
    try:
        resulf_df = pd.DataFrame(columns=["date", "rsi"])
        closes = df.close
        # print(closes)
        for i in range(0, df.shape[0], PERIOD):
            U = 0
            D = 0
            if i + PERIOD > df.shape[0]:
                closes_now = closes[i:].to_list()
            else:
                closes_now = list(closes[i : i + PERIOD])
            # print(closes_now)
            for j in range(len(closes_now) - 1):
                # print("xzxzxzx", closes_now[j + 1] - closes_now[j])
                if closes_now[j + 1] - closes_now[j] < 0:
                    D += closes_now[j + 1] - closes_now[j]
                else:
                    U += closes_now[j + 1] - closes_now[j]
            try:
                rs = (U / PERIOD) / (-D / PERIOD)
            except:
                rs = (U / PERIOD) / (0.0000001)
            if (i + i + PERIOD) // 2 > df.shape[0]:
                date = df.date[df.shape[0] - 1]
            else:
                date = df.date[(i + i + PERIOD) // 2]
            rsi = 100 - (100 / (1 + rs))
            resulf_df.loc[resulf_df.shape[0]] = (date, rsi)
        resulf_df.apply(lambda x: add_row_metric(x, symbol, "rsi"), axis=1)
    except Exception as e:
        print(f"Error in calculate_rsi : {e}")


def calculate_ema(values, window=14):
    alpha = 2 / (window + 1)
    ema_values = np.zeros_like(values, dtype=float)
    ema_values[0] = values[0]

    for i in range(1, len(values)):
        ema_values[i] = alpha * values[i] + (1 - alpha) * ema_values[i - 1]

    return ema_values


def calculate_macd(df: pd.DataFrame, symbol):
    window_fast = 12
    window_slow = 26
    result_df = pd.DataFrame(columns=["date", "macd", "signal"])
    values_full = df.close.to_list()
    dates = df.date.to_list()
    # print(dates[-100:])
    for i in range(0, df.shape[0], PERIOD):
        # print(df.shape[0], i)
        if i + PERIOD > df.shape[0]:
            date = dates[df.shape[0] - 1]
            values = values_full[i:]
        else:
            date = dates[(i + i + PERIOD) // 2]
            values = values_full[i : i + PERIOD]
        # print(date)
        fast_ma = calculate_ema(values, window_fast)
        slow_ma = calculate_ema(values, window_slow)

        macd = fast_ma - slow_ma
        signal_window = 9
        signal = calculate_ema(macd, signal_window)
        coef_macd = macd.mean()
        coef_signal = signal.mean()
        result_df.loc[result_df.shape[0]] = [date, coef_macd, coef_signal]
    result_df.apply(lambda x: add_row_macd(x, symbol), axis=1)


def start_calc_metrics():
    tables = ["apple", "ibm", "microsoft"]
    for table in tables:
        delete_from_table(f"{table}_macd")
        print(f"remove {table}_macd")
        delete_from_table(f"{table}_rsi")
        print(f"remove {table}_rsi")
        delete_from_table(f"{table}_ma")
        print((f"remove {table}_ma"))

        df = get_table_for_metrics(table)

        calculate_ma(df, table)
        calculate_rsi(df, table)
        calculate_macd(df, table)
