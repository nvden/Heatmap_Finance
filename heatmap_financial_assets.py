# requirements:
# pip install yfinance plotly pandas streamlit

import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import datetime

# Активы и тикеры
assets = {
    "S&P 500": "^GSPC",
    "Nasdaq": "^IXIC",
    "Nikkei": "^N225",
    "CSI 500": "000905.SS",
    "Stoxx50": "^STOXX50E",
    "Gold": "GC=F",
    "Oil Brent": "BZ=F",
    "DXY": "DX-Y.NYB",
    "VIX": "^VIX",
    "US10Y": "^TNX",
    "Bitcoin": "BTC-USD",
    "Ethereum": "ETH-USD",
    "Solana": "SOL-USD"
}

# Функция для получения изменений за 1 день и 1 неделю
def fetch_changes(ticker):
    end = datetime.datetime.today()
    start = end - datetime.timedelta(days=8)  # чтобы точно захватить неделю назад
    df = yf.download(ticker, start=start, end=end)

    if len(df) < 2:
        return None, None

    change_1d = ((df["Close"][-1] - df["Close"][-2]) / df["Close"][-2]) * 100 if len(df) >= 2 else None
    change_1w = ((df["Close"][-1] - df["Close"][0]) / df["Close"][0]) * 100 if len(df) >= 5 else None

    return change_1d, change_1w

# Получение данных
records = []
for name, ticker in assets.items():
    change_1d, change_1w = fetch_changes(ticker)
    records.append({
        "Asset": name,
        "1D %": change_1d,
        "1W %": change_1w
    })

df = pd.DataFrame(records)

# Построение тепловой карты
fig = go.Figure()

for i, row in df.iterrows():
    text = f"{row['Asset']}\n1D: {row['1D %']:.2f}%\n1W: {row['1W %']:.2f}%"
    color = "#d62728" if row['1D %'] < 0 else "#2ca02c"
    fig.add_trace(go.Scatter(
        x=[i % 4], y=[-(i // 4)],
        mode="markers+text",
        marker=dict(size=100, color=color, opacity=0.6),
        text=[text], textposition="middle center"
    ))

fig.update_layout(
    title="Тепловая карта по финансовым активам",
    xaxis=dict(visible=False),
    yaxis=dict(visible=False),
    plot_bgcolor="white",
    height=600
)

fig.show()
