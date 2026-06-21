import streamlit as st
import pandas as pd
import plotly.express as px
st.set_page_config(page_title="Global Stock Market Analysis", layout="wide")
st.markdown("""
<style>
.main {
    background-color: #f8f9fb;
}
.block-container {
    padding-top: 2rem;
}
.metric-card {
    background-color: white;
    padding: 20px;
    border-radius: 14px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.08);
}
.section-box {
    background-color: white;
    padding: 25px;
    border-radius: 16px;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.06);
    margin-bottom: 25px;
}
</style>
""", unsafe_allow_html=True)

st.title("Global Stock Market Analysis")
st.write("This dashboard provides an analysis of the global stock market, including trends, performance, and key insights.")
dataset = pd.read_csv("cleaned_stock_data.csv")

dataset["Date"] = pd.to_datetime(dataset["Date"])

ticker = st.selectbox(
    "Select a Stock",
    sorted(dataset["Ticker"].dropna().unique())
)

stock = dataset[dataset["Ticker"] == ticker].copy()

stock["Daily Return"] = stock["Close"].pct_change() * 100
stock["MA 20"] = stock["Close"].rolling(window=20).mean()
stock["MA 50"] = stock["Close"].rolling(window=50).mean()

latest_price = stock["Close"].iloc[-1]
previous_price = stock["Close"].iloc[-2]
daily_change_pct = ((latest_price - previous_price) / previous_price) * 100
high_52 = stock.tail(252)["High"].max()
low_52 = stock.tail(252)["Low"].min()
avg_volume = stock["Volume"].mean()
total_return = ((stock["Close"].iloc[-1] - stock["Close"].iloc[0]) / stock["Close"].iloc[0]) * 100
volatility = stock["Daily Return"].std()

st.subheader(f"{ticker} Key Metrics")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Latest Close", f"${latest_price:,.2f}", f"{daily_change_pct:.2f}%")
col2.metric("52-Week High", f"${high_52:,.2f}")
col3.metric("52-Week Low", f"${low_52:,.2f}")
col4.metric("Average Volume", f"{avg_volume:,.0f}")

col5, col6, col7, col8 = st.columns(4)
col5.metric("Total Return", f"{total_return:.2f}%")
col6.metric("Volatility", f"{volatility:.2f}%")
col7.metric("First Date", stock["Date"].min().strftime("%Y-%m-%d"))
col8.metric("Latest Date", stock["Date"].max().strftime("%Y-%m-%d"))

fig_price = px.line(
    stock,
    x="Date",
    y=["Close", "MA 20", "MA 50"],
    title=f"{ticker} Closing Price with Moving Averages"
)
st.plotly_chart(fig_price, use_container_width=True)

left_col, right_col = st.columns(2)

with left_col:
    fig_volume = px.bar(
        stock,
        x="Date",
        y="Volume",
        title=f"{ticker} Trading Volume"
    )
    st.plotly_chart(fig_volume, use_container_width=True)

with right_col:
    fig_returns = px.histogram(
        stock.dropna(),
        x="Daily Return",
        nbins=50,
        title=f"{ticker} Daily Return Distribution"
    )
    st.plotly_chart(fig_returns, use_container_width=True)

fig_ohlc = px.line(
    stock,
    x="Date",
    y=["Open", "High", "Low", "Close"],
    title=f"{ticker} Open, High, Low, and Close Prices"
)
st.plotly_chart(fig_ohlc, use_container_width=True)

st.subheader(f"{ticker} Recent Data")
recent_data = stock.sort_values(
    "Date",
    ascending=False
).head(10)

st.dataframe(recent_data, use_container_width=True)