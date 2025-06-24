# requirements:
# pip install yfinance plotly pandas streamlit

import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import datetime
import streamlit as st

# Активы и тикеры
assets = {
    "S&P 500": "^GSPC",
    "Nasdaq": "^IXIC",
    "Nikkei": "^N225",
    "CSI 500": "000905.SS",
    "Gold": "GC=F",
    "Oil Brent": "BZ=F",
    "DXY": "DX-Y.NYB",
    "Bitcoin": "BTC-USD",
    "Ethereum": "ETH-USD",
    "Solana": "SOL-USD"
}

# Функция для получения изменений за 1 день и 1 неделю
def fetch_changes(ticker):
    end = datetime.datetime.today()
    start = end - datetime.timedelta(days=10)
    df = yf.download(ticker, start=start, end=end)
    st.write(f"Данные для {ticker}:")
    st.write(df)

    if df.empty:
        return None, None

    # Убедимся, что колонка Close есть
    if "Close" not in df.columns:
        return None, None

    df = df.copy()
    df = df[~df["Close"].isna()]

    change_1d = None
    change_1w = None

    if len(df) >= 2:
        change_1d = ((df["Close"].iloc[-1] - df["Close"].iloc[-2]) / df["Close"].iloc[-2]) * 100
    if len(df) >= 5:
        change_1w = ((df["Close"].iloc[-1] - df["Close"].iloc[0]) / df["Close"].iloc[0]) * 100

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
st.write("Итоговая таблица изменений:")
st.write(df)  # Отладочный вывод данных

# Построение тепловой карты
fig = go.Figure()

for i, row in df.iterrows():
    try:
        if pd.isna(row['1D %']) and pd.isna(row['1W %']):
            continue
        text = f"{row['Asset']}\n1D: {row['1D %']:.2f}%\n1W: {row['1W %']:.2f}%"
        color = "#d62728" if row['1D %'] is not None and row['1D %'] < 0 else "#2ca02c"
        fig.add_trace(go.Scatter(
            x=[i % 4], y=[-(i // 4)],
            mode="markers+text",
            marker=dict(size=100, color=color, opacity=0.6),
            text=[text], textposition="middle center"
        ))
    except Exception as e:
        continue

fig.update_layout(
    title="Тепловая карта по финансовым активам",
    xaxis=dict(visible=False),
    yaxis=dict(visible=False),
    plot_bgcolor="white",
    height=600
)

st.title("📈 Тепловая карта по финансовым активам")
st.plotly_chart(fig, use_container_width=True)
