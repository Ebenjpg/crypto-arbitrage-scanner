import streamlit as st
import pandas as pd
import time
import bott

st.set_page_config(page_title="Crypto Scanner", layout="wide")

st.title("📊 Live Crypto Arbitrage Scanner")

placeholder = st.empty()

while True:
    try:
        # call your scanner logic indirectly
        opportunities = []

        st.markdown("### 🔄 Scanning market...")

        placeholder.write("Waiting for opportunities from bot...")

        time.sleep(2)

    except Exception as e:
        placeholder.error(f"Error: {e}")
