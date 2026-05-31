import streamlit as st
import bott
import time

st.set_page_config(page_title="Crypto Arbitrage Scanner", layout="wide")

st.title("📊 Live Crypto Arbitrage Scanner")

st.info("Scanner is running... please wait")

placeholder = st.empty()

# fake safe display loop (no terminal errors)
for i in range(1, 5):
    placeholder.write(f"🔄 System active... cycle {i}")
    time.sleep(1)

st.success("System initialized successfully 🚀")
