# pages/4_settings.py
import streamlit as st
import pandas as pd
import subprocess
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ---- Load Styles ----
css_path = os.path.join(os.path.dirname(__file__), "..", "styles.css")
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
else:
    st.warning(f"⚠ styles.css not found at {css_path}")

# ---- Page Header ----
st.header("⚙ Settings & Pipeline Control")
st.write("Re-run the pipeline (scrape → NLP → forecast)")

# ---- Run Pipeline Button ----
if st.button("🔄 Run Pipeline"):
    with st.spinner("Running... This may take 1–2 minutes"):
        try:
            subprocess.run([sys.executable, "app.py"], check=True)
            subprocess.run([sys.executable, "nlp/keywords.py"], check=True)
            subprocess.run([sys.executable, "nlp/sentiment.py"], check=True)
            subprocess.run([sys.executable, "forecast/forecast.py"], check=True)
            st.success("✅ Pipeline finished! Reload pages to see updates.")
        except Exception as e:
            st.error(f"❌ Pipeline failed: {e}")

# ---- Download Raw Data ----
data_path = os.path.join("data", "reddit_posts.csv")
if os.path.exists(data_path):
    df = pd.read_csv(data_path)
    st.download_button(
        "⬇ Download Raw Data",
        df.to_csv(index=False).encode('utf-8'),
        file_name="reddit_posts.csv"
    )
else:
    st.warning("reddit_posts.csv not found.")
