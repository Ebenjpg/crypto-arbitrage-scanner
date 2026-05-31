import streamlit as st
import bott
import time

st.title("📊 Live Crypto Arbitrage Scanner")

placeholder = st.empty()

while True:
    try:
        # we will connect real data here next step
        placeholder.write("🔄 Scanner running... waiting for live data")

        time.sleep(2)

    except Exception as e:
        placeholder.write(f"Error: {e}")
