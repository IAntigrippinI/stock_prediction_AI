import plotly.graph_objects as go
from calculate_metrics import calculate_macd, calculate_signal_line
from df import df


fig = go.Figure()

fig.update_layout(title='MADC', xaxis_rangeslider_visible=False)


fig.add_trace(go.Scatter(x=df.index, y=(calculate_macd(df.close)), mode='lines', name='MACD'))
fig.add_trace(go.Scatter(x=df.index, y=(calculate_signal_line(df.close)), mode='lines', name='Signal line'))
print(df[df.close.isna()])
fig.show()