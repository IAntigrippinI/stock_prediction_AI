import plotly.graph_objects as go
from calculate_metrics import calculate_ma
from df import df


fig = go.Figure(data=[go.Candlestick(x=df.index,
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'])])

fig.update_layout(title='Day OHLC Candlestick Chart', xaxis_rangeslider_visible=False)

fig.add_trace(go.Scatter(x=df.index, y=calculate_ma(df.close), mode='lines', name='MA'))

print(df[df.close.isna()])
fig.show()