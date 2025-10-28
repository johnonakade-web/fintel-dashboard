import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import plotly.express as px

st.set_page_config(page_title="Stock Lending Rate Dashboard (Fintel)", layout="wide")

st.sidebar.header("Settings")
tickers_input = st.sidebar.text_area(
    "Enter tickers (comma-separated):", "AAPL, TSLA, AMC, GME"
)
tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]
refresh = st.sidebar.button("🔄 Refresh Data")

@st.cache_data(ttl=600)
def get_fintel_borrow_rate(ticker):
    try:
        url = f"https://fintel.io/api/borrow-rates?ticker={ticker}"
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            data = r.json()
            return {
                "ticker": ticker,
                "borrow_fee_rate": data.get("borrow_fee_rate"),
                "available": data.get("available"),
                "timestamp": datetime.utcnow(),
            }
        else:
            return {"ticker": ticker, "borrow_fee_rate": None, "available": None}
    except Exception as e:
        st.warning(f"Error fetching {ticker}: {e}")
        return {"ticker": ticker, "borrow_fee_rate": None, "available": None}

if refresh:
    with st.spinner("Fetching data from Fintel..."):
        results = [get_fintel_borrow_rate(t) for t in tickers]
        df = pd.DataFrame(results)
        st.session_state["data"] = df

if "data" in st.session_state and not st.session_state["data"].empty:
    df = st.session_state["data"]
    st.subheader("📊 Borrow / Lending Rates (Fintel.io)")
    st.dataframe(df, use_container_width=True)
    fig = px.bar(
        df,
        x="ticker",
        y="borrow_fee_rate",
        title="Borrow Fee Rate by Ticker",
        text_auto=".2f",
        labels={"borrow_fee_rate": "Borrow Fee Rate (%)"},
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Enter tickers and click **Refresh Data** to begin.")
