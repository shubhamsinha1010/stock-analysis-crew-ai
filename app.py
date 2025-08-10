import sys
import pysqlite3
sys.modules['sqlite3'] = pysqlite3
import streamlit as st
from dotenv import load_dotenv
from crew import stock_crew
import re
import yfinance as yf
import pandas as pd

# Load environment variables
load_dotenv()

st.set_page_config(page_title="📈 AI Stock Research", layout="centered")
st.title("📈 AI Stock Research Tool")
st.write("Enter one or more stock symbols (comma-separated) to compare:")

# Multi-stock input
stocks_input = st.text_input("Stock Symbols", value="AAPL,MSFT", max_chars=50)
stock_list = [s.strip().upper() for s in stocks_input.split(",") if s.strip()]

if st.button("Compare"):
    cols = st.columns(len(stock_list))
    for idx, stock in enumerate(stock_list):
        with cols[idx]:
            st.subheader(stock)
            with st.spinner(f"Analyzing {stock}..."):
                # Run the crew and get result
                result = stock_crew.kickoff(inputs={"stock": stock})

                # Detect type: CrewOutput object or dict
                if hasattr(result, "model_dump"):
                    result_dict = result.model_dump()
                    tasks_output = getattr(result, "tasks_output", result_dict.get("tasks_output", []))
                elif isinstance(result, dict):
                    result_dict = result
                    tasks_output = result.get("tasks_output", [])
                else:
                    st.error("Unexpected result type.")
                    continue

                if not tasks_output or len(tasks_output) < 2:
                    st.error("AI did not return expected output.")
                    continue

                performance = tasks_output[0]
                recommendation = tasks_output[1]
                perf_raw = performance.get("raw") if isinstance(performance, dict) else getattr(performance, "raw", "")
                rec_raw = recommendation.get("raw") if isinstance(recommendation, dict) else getattr(recommendation, "raw", "")

                price_match = re.search(r"(\d{1,3}(?:,\d{3})*(?:\.\d+)?)\s*USD", perf_raw)
                price = float(price_match.group(1).replace(",", "")) if price_match else None
                change_match = re.search(r"price change.*?([\d\.]+)", perf_raw)
                change = float(change_match.group(1)) if change_match else None
                percent_match = re.search(r"\(([\d\.]+)%\)", perf_raw)
                percent_change = float(percent_match.group(1)) if percent_match else None
                volume_match = re.search(r"trading volume of ([\d,]+)", perf_raw)
                volume = int(volume_match.group(1).replace(",", "")) if volume_match else None

                st.metric("Price (USD)", f"${price}" if price else "N/A")
                st.metric("Change", f"${change}" if change else "N/A", delta=f"{percent_change}%" if percent_change else None)
                st.metric("Volume", f"{volume:,}" if volume else "N/A")
                st.caption("Recommendation:")
                st.markdown(rec_raw)

                # Historical Data Visualization
                data = yf.download(stock, period="6mo")
                if not data.empty:
                    if isinstance(data.columns, pd.MultiIndex):
                        data.columns = ['_'.join(col).strip() if isinstance(col, tuple) else col for col in data.columns]
                    close_col = [col for col in data.columns if "Close" in col][0]
                    data["MA20"] = data[close_col].rolling(window=20).mean()
                    data["MA50"] = data[close_col].rolling(window=50).mean()
                    ma_data = data[[close_col, "MA20", "MA50"]].dropna()
                    st.line_chart(ma_data, use_container_width=True)
                else:
                    st.warning("No historical data found.")

                # News Integration
                st.caption("Recent News")
                try:
                    news_items = yf.Ticker(stock).get_news()
                    if news_items:
                        for item in news_items[:3]:
                            title = item.get("title")
                            link = item.get("link")
                            if title and link:
                                st.markdown(f"- [{title}]({link})")
                            if item.get("publisher"):
                                st.caption(f"Source: {item['publisher']}")
                    else:
                        st.info("No news found.")
                except Exception as e:
                    st.error(f"Error fetching news: {e}")

# --- Single Stock Analysis (legacy) ---
st.write("---")
st.write("Or analyze a single stock symbol below:")
stock = st.text_input("Stock Symbol", value="AAPL", max_chars=10, key="single_stock")

if st.button("Analyze"):
    with st.spinner("Analyzing..."):
        result = stock_crew.kickoff(inputs={"stock": stock})
        if hasattr(result, "model_dump"):
            result_dict = result.model_dump()
            tasks_output = getattr(result, "tasks_output", result_dict.get("tasks_output", []))
        elif isinstance(result, dict):
            result_dict = result
            tasks_output = result.get("tasks_output", [])
        else:
            st.error("Unexpected result type.")
            st.stop()

        if not tasks_output or len(tasks_output) < 2:
            st.error("The AI did not return the expected tasks output.")
            st.stop()

        performance = tasks_output[0]
        recommendation = tasks_output[1]
        perf_raw = performance.get("raw") if isinstance(performance, dict) else getattr(performance, "raw", "")
        rec_raw = recommendation.get("raw") if isinstance(recommendation, dict) else getattr(recommendation, "raw", "")

        price_match = re.search(r"(\d{1,3}(?:,\d{3})*(?:\.\d+)?)\s*USD", perf_raw)
        price = float(price_match.group(1).replace(",", "")) if price_match else None
        change_match = re.search(r"price change.*?([\d\.]+)", perf_raw)
        change = float(change_match.group(1)) if change_match else None
        percent_match = re.search(r"\(([\d\.]+)%\)", perf_raw)
        percent_change = float(percent_match.group(1)) if percent_match else None
        volume_match = re.search(r"trading volume of ([\d,]+)", perf_raw)
        volume = int(volume_match.group(1).replace(",", "")) if volume_match else None

        st.success("✅ Analysis Complete!")
        st.header("📊 Stock Performance Summary")
        col1, col2, col3 = st.columns(3)
        col1.metric("Current Price (USD)", f"${price}" if price else "N/A")
        col2.metric("Daily Change", f"${change}" if change else "N/A",
                    delta=f"{percent_change}%" if percent_change else None)
        col3.metric("Trading Volume", f"{volume:,}" if volume else "N/A")

        st.subheader("📌 Key Observations")
        st.markdown(perf_raw)
        st.subheader("🎯 Strategic Recommendation")
        st.markdown(rec_raw)

        st.subheader("📈 Price History & Volume Trends (6 months)")
        data = yf.download(stock, period="6mo")
        if not data.empty:
            if isinstance(data.columns, pd.MultiIndex):
                data.columns = ['_'.join(col).strip() if isinstance(col, tuple) else col for col in data.columns]
            close_col = [col for col in data.columns if "Close" in col][0]
            data["MA20"] = data[close_col].rolling(window=20).mean()
            data["MA50"] = data[close_col].rolling(window=50).mean()
            ma_data = data[[close_col, "MA20", "MA50"]].dropna()
            st.write("Closing Price")
            st.line_chart(data[close_col], use_container_width=True)
            st.write("Trading Volume")
            vol_col = [col for col in data.columns if "Volume" in col][0]
            st.line_chart(data[vol_col], use_container_width=True)
            st.write("Moving Averages (20 & 50 days)")
            st.line_chart(ma_data, use_container_width=True)
        else:
            st.warning("No historical data found for this symbol.")

        st.subheader("📰 Recent News Headlines")
        try:
            news_items = yf.Ticker(stock).get_news()
            if news_items:
                for item in news_items[:5]:
                    title = item.get("title")
                    link = item.get("link")
                    if title and link:
                        st.markdown(f"- [{title}]({link})")
                    if item.get("publisher"):
                        st.caption(f"Source: {item['publisher']}")
            else:
                st.info("No recent news found for this symbol.")
        except Exception as e:
            st.error(f"Error fetching news: {e}")