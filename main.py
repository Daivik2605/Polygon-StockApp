import streamlit as st
import pandas as pd
from polygon import RESTClient
import plotly.graph_objects as go

st.title("📊 Polygon + Streamlit Demo App")

# --- Inputs ---
symbol = st.text_input("Enter a stock symbol", "AAPL")

with st.sidebar:
    st.write("🔑 Enter your Polygon API Key")
    polygon_api_key = st.text_input("API Key", type="password")

# --- Authenticate ---
client = None
if polygon_api_key.strip():
    client = RESTClient(polygon_api_key)
else:
    st.warning("⚠️ Please enter your API key in the sidebar to use the app.")

# --- Buttons ---
col1, col2, col3 = st.columns(3)

# Stock details with fundamentals
import requests

if col1.button("Get Details"):
    if not polygon_api_key.strip() or not symbol.strip():
        st.error("Missing API key or symbol.")
    else:
        try:
            # --- Company Info ---
            details = client.get_ticker_details(symbol)
            st.subheader("📌 Company Details")
            st.write(f"**Ticker:** {details.ticker}")
            st.write(f"**Name:** {details.name}")
            st.write(f"**Market Cap:** {details.market_cap:,}")
            st.write(f"**Homepage:** {details.homepage_url}")

            # --- Fundamentals via REST API ---
            url = f"https://api.polygon.io/vX/reference/financials?ticker={symbol}&limit=1&apiKey={polygon_api_key}"
            response = requests.get(url)
            data = response.json()

            if "results" in data and len(data["results"]) > 0:
                fundamentals = data["results"][0]["financials"]

                income = fundamentals.get("income_statement", {})
                ratios = fundamentals.get("ratios", {})

                # Dashboard metrics
                st.subheader("📊 Key Financial Metrics")
                colA, colB, colC = st.columns(3)
                colA.metric("Revenue", f"{income.get('revenues', 'N/A')}")
                colB.metric("Net Income", f"{income.get('net_income', 'N/A')}")
                colC.metric("EPS", f"{income.get('eps', 'N/A')}")

                colD, colE, colF = st.columns(3)
                colD.metric("P/E Ratio", f"{ratios.get('peRatioTTM', 'N/A')}")
                colE.metric("Gross Margin", f"{ratios.get('grossMargin', 'N/A')}")
                colF.metric("Dividend Yield", f"{ratios.get('dividendYield', 'N/A')}")

                # Expandable table of all fundamentals
                st.subheader("📑 Full Financial Data")
                df = pd.json_normalize(fundamentals)
                st.dataframe(df.T, use_container_width=True)

            else:
                st.info("No financial data available for this symbol.")

        except Exception as e:
            st.exception(e)





# --- Previous close quote ---
if col2.button("Get Quote"):
    if not client or not symbol.strip():
        st.error("Missing API key or symbol.")
    else:
        try:
            aggs = client.get_previous_close_agg(symbol)
            st.subheader("📉 Previous Close Data")
            df_quote = pd.DataFrame([agg.__dict__ for agg in aggs])
            st.dataframe(df_quote[["ticker", "open", "high", "low", "close", "volume"]])
        except Exception as e:
            st.exception(e)

# --- Historical chart ---
if col3.button("Get Historical"):
    if not client or not symbol.strip():
        st.error("Missing API key or symbol.")
    else:
        try:
            # Dynamic date range (last 5 years to today)
            end_date = pd.Timestamp.now().strftime("%Y-%m-%d")
            start_date = (pd.Timestamp.now() - pd.DateOffset(years=5)).strftime("%Y-%m-%d")

            data = list(client.list_aggs(
                ticker=symbol,
                multiplier=1,
                timespan="day",
                from_=start_date,
                to=end_date
            ))

            chart_data = pd.DataFrame([d.__dict__ for d in data])
            chart_data["date"] = pd.to_datetime(chart_data["timestamp"], unit="ms")

            # Sort by date
            chart_data = chart_data.sort_values("date")

            st.subheader(f"📈 {symbol} Price Trend (Last 5 Years)")
            st.line_chart(chart_data, x="date", y="close")

            # Add a data table
            st.subheader("📋 Historical Data Table")
            st.dataframe(
                chart_data[["date", "open", "high", "low", "close", "volume"]].set_index("date"),
                use_container_width=True
            )

            # Optional: add rolling average
            chart_data["50d_ma"] = chart_data["close"].rolling(window=50).mean()
            chart_data["200d_ma"] = chart_data["close"].rolling(window=200).mean()

            st.line_chart(chart_data, x="date", y=["close", "50d_ma", "200d_ma"])

        except Exception as e:
            st.exception(e)
