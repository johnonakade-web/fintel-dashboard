{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import streamlit as st\
import pandas as pd\
import requests\
from datetime import datetime\
import plotly.express as px\
\
st.set_page_config(page_title="Stock Lending Rate Dashboard (Fintel)", layout="wide")\
\
st.sidebar.header("Settings")\
tickers_input = st.sidebar.text_area(\
    "Enter tickers (comma-separated):", "AAPL, TSLA, AMC, GME"\
)\
tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]\
refresh = st.sidebar.button("\uc0\u55357 \u56580  Refresh Data")\
\
@st.cache_data(ttl=600)\
def get_fintel_borrow_rate(ticker):\
    try:\
        url = f"https://fintel.io/api/borrow-rates?ticker=\{ticker\}"\
        r = requests.get(url, timeout=10)\
        if r.status_code == 200:\
            data = r.json()\
            return \{\
                "ticker": ticker,\
                "borrow_fee_rate": data.get("borrow_fee_rate"),\
                "available": data.get("available"),\
                "timestamp": datetime.utcnow(),\
            \}\
        else:\
            return \{"ticker": ticker, "borrow_fee_rate": None, "available": None\}\
    except Exception as e:\
        st.warning(f"Error fetching \{ticker\}: \{e\}")\
        return \{"ticker": ticker, "borrow_fee_rate": None, "available": None\}\
\
if refresh:\
    with st.spinner("Fetching data from Fintel..."):\
        results = [get_fintel_borrow_rate(t) for t in tickers]\
        df = pd.DataFrame(results)\
        st.session_state["data"] = df\
\
if "data" in st.session_state and not st.session_state["data"].empty:\
    df = st.session_state["data"]\
    st.subheader("\uc0\u55357 \u56522  Borrow / Lending Rates (Fintel.io)")\
    st.dataframe(df, use_container_width=True)\
    fig = px.bar(\
        df,\
        x="ticker",\
        y="borrow_fee_rate",\
        title="Borrow Fee Rate by Ticker",\
        text_auto=".2f",\
        labels=\{"borrow_fee_rate": "Borrow Fee Rate (%)"\},\
    )\
    st.plotly_chart(fig, use_container_width=True)\
else:\
    st.info("Enter tickers and click **Refresh Data** to begin.")\
}