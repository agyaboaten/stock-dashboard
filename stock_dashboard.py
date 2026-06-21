import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(page_title="Global Stock Market Analysis", layout="wide")

st.markdown(
    """
    <style>
    .main {
        background-color: #f8f9fb;
    }
    .block-container {
        padding-top: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_data():
    dataset = pd.read_csv("cleaned_stock_data.csv")
    dataset["Date"] = pd.to_datetime(dataset["Date"], utc=True)
    return dataset.sort_values("Date")


dataset = load_data()

st.title("Global Stock Market Analysis")
st.write(
    "Explore historical stock market trends, performance, and key metrics "
    "from a cleaned global stock dataset."
)

# Sidebar filters narrow the dashboard before a stock is selected.
st.sidebar.header("Filters")

countries = sorted(dataset["Country"].dropna().unique())
selected_countries = st.sidebar.multiselect(
    "Country",
    countries,
    default=countries,
)

country_filtered = dataset[dataset["Country"].isin(selected_countries)]

if country_filtered.empty:
    st.warning("Select at least one country to view dashboard data.")
    st.stop()

industries = sorted(country_filtered["Industry_Tag"].dropna().unique())
selected_industries = st.sidebar.multiselect(
    "Industry",
    industries,
    default=industries,
)

filtered_data = country_filtered[
    country_filtered["Industry_Tag"].isin(selected_industries)
].copy()

if filtered_data.empty:
    st.warning("Select at least one industry to view dashboard data.")
    st.stop()

min_date = filtered_data["Date"].min().date()
max_date = filtered_data["Date"].max().date()
date_range = st.sidebar.date_input(
    "Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

if len(date_range) != 2:
    st.warning("Select both a start date and an end date.")
    st.stop()

start_date, end_date = date_range

filtered_data = filtered_data[
    (filtered_data["Date"].dt.date >= start_date)
    & (filtered_data["Date"].dt.date <= end_date)
]

if filtered_data.empty:
    st.warning("No data is available for the selected filters.")
    st.stop()

ticker_options = sorted(filtered_data["Ticker"].dropna().unique())
ticker = st.selectbox("Select a Stock", ticker_options)

stock = filtered_data[filtered_data["Ticker"] == ticker].copy()
stock = stock.sort_values("Date")

if len(stock) < 2:
    st.warning("This stock needs at least two records to calculate performance metrics.")
    st.dataframe(stock, use_container_width=True)
    st.stop()

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

company_name = stock["Brand_Name"].iloc[-1].title()
industry = stock["Industry_Tag"].iloc[-1].title()
country = stock["Country"].iloc[-1].title()

st.subheader(f"{ticker} - {company_name}")
st.caption(f"{industry} | {country}")

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
    title=f"{ticker} Closing Price with Moving Averages",
)
st.plotly_chart(fig_price, use_container_width=True)

left_col, right_col = st.columns(2)

with left_col:
    fig_volume = px.bar(
        stock,
        x="Date",
        y="Volume",
        title=f"{ticker} Trading Volume",
    )
    st.plotly_chart(fig_volume, use_container_width=True)

with right_col:
    fig_returns = px.histogram(
        stock.dropna(),
        x="Daily Return",
        nbins=50,
        title=f"{ticker} Daily Return Distribution",
    )
    st.plotly_chart(fig_returns, use_container_width=True)

fig_ohlc = px.line(
    stock,
    x="Date",
    y=["Open", "High", "Low", "Close"],
    title=f"{ticker} Open, High, Low, and Close Prices",
)
st.plotly_chart(fig_ohlc, use_container_width=True)

st.subheader("Compare Stocks")
comparison_tickers = st.multiselect(
    "Select stocks to compare",
    ticker_options,
    default=[ticker],
)

if comparison_tickers:
    comparison_data = filtered_data[
        filtered_data["Ticker"].isin(comparison_tickers)
    ].sort_values("Date")

    fig_comparison = px.line(
        comparison_data,
        x="Date",
        y="Close",
        color="Ticker",
        title="Closing Price Comparison",
    )
    st.plotly_chart(fig_comparison, use_container_width=True)

st.subheader(f"{ticker} Recent Data")
recent_data = stock.sort_values("Date", ascending=False).head(10)
st.dataframe(recent_data, use_container_width=True)

csv_data = stock.to_csv(index=False).encode("utf-8")
st.download_button(
    "Download Selected Stock Data",
    data=csv_data,
    file_name=f"{ticker}_stock_data.csv",
    mime="text/csv",
)
