import pandas as pd
import numpy as np



def calculate_rsi(prices, n=14):
    deltas = np.diff(prices)
    seed = deltas[:n+1]
    up = seed[seed >= 0].sum() / n
    down = -seed[seed < 0].sum() / n
    rs = up / down
    rsi = np.zeros_like(prices)
    rsi[:n] = 100. - 100. / (1. + rs)

    for i in range(n, len(prices)):
        delta = deltas[i - 1]  
        if delta > 0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta

        up = (up * (n - 1) + upval) / n
        down = (down * (n - 1) + downval) / n

        rs = up / down
        rsi[i] = 100. - 100. / (1. + rs)

    return rsi




def calculate_ma(values, window = 14):
    moving_averages = []
    for i in range(len(values) - window + 1):
        window_values = values[i : i + window]
        window_average = sum(window_values) / window
        moving_averages.append(window_average)
    return moving_averages


#экспоненциальное сглаживание
def calculate_ema(values, window=14):
    alpha = 2 / (window + 1)
    ema_values = np.zeros_like(values, dtype=float)
    ema_values[0] = values[0]
    
    for i in range(1, len(values)):
        ema_values[i] = alpha * values[i] + (1 - alpha) * ema_values[i-1]
    
    return ema_values


def calculate_macd(values, window_slow=26, window_fast=12):
    fast_ma = calculate_ema(values, window_fast)
    slow_ma = calculate_ema(values, window_slow)
    macd = fast_ma - slow_ma
    return macd

def calculate_signal_line(values, signal_window = 9, window_slow=26, window_fast=12):
    return calculate_ema(calculate_macd(values, window_slow, window_fast), signal_window)

