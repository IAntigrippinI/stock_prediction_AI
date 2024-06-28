import plotly.graph_objects as go
from calculate_metrics import calculate_rsi, calculate_ema
from df import df




# Создание графика свечей 
fig = go.Figure(data=[go.Candlestick(x=df.index,
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'])])

fig.update_layout(title='Day OHLC Candlestick Chart', xaxis_rangeslider_visible=False)

# Добавление RSI на график
fig.add_trace(go.Scatter(x=df.index, y=calculate_rsi(df.close), mode='lines', name='RSI'))


fig.show()