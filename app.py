import sys
import pysqlite3
sys.modules['sqlite3'] = pysqlite3
import streamlit as st
from dotenv import load_dotenv
from crew import stock_crew
import json
import re

# Load environment variables
load_dotenv()

# Streamlit page config
st.set_page_config(page_title="📈 AI Stock Research", layout="centered")

st.title("📈 AI Stock Research Tool")
st.write("Enter a stock symbol to get AI-powered research insights.")

# Stock symbol input
stock = st.text_input("Stock Symbol", value="AAPL", max_chars=10)

if st.button("Analyze"):
    with st.spinner("Analyzing..."):
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
            st.stop()

        if not tasks_output or len(tasks_output) < 2:
            st.error("The AI did not return the expected tasks output.")
            st.stop()

        # Extract performance & recommendation objects
        performance = tasks_output[0]
        recommendation = tasks_output[1]

        # Handle both dict and object
        perf_raw = performance.get("raw") if isinstance(performance, dict) else getattr(performance, "raw", "")
        rec_raw = recommendation.get("raw") if isinstance(recommendation, dict) else getattr(recommendation, "raw", "")

        # Parse values from the raw text if not provided in JSON
        price_match = re.search(r"(\d{1,3}(?:,\d{3})*(?:\.\d+)?)\s*USD", perf_raw)
        price = float(price_match.group(1).replace(",", "")) if price_match else None

        change_match = re.search(r"price change.*?([\d\.]+)", perf_raw)
        change = float(change_match.group(1)) if change_match else None

        percent_match = re.search(r"\(([\d\.]+)%\)", perf_raw)
        percent_change = float(percent_match.group(1)) if percent_match else None

        volume_match = re.search(r"trading volume of ([\d,]+)", perf_raw)
        volume = int(volume_match.group(1).replace(",", "")) if volume_match else None

        # Display results
        st.success("✅ Analysis Complete!")

        # Stock performance metrics
        st.header("📊 Stock Performance Summary")
        col1, col2, col3 = st.columns(3)
        col1.metric("Current Price (USD)", f"${price}" if price else "N/A")
        col2.metric("Daily Change", f"${change}" if change else "N/A",
                    delta=f"{percent_change}%" if percent_change else None)
        col3.metric("Trading Volume", f"{volume:,}" if volume else "N/A")

        # Observations
        st.subheader("📌 Key Observations")
        st.markdown(perf_raw)

        # Recommendation
        st.subheader("🎯 Strategic Recommendation")
        st.markdown(rec_raw)
