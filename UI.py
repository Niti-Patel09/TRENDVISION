# ui.py — root home page (lightweight nav & shared data)
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os
from streamlit_autorefresh import st_autorefresh
from streamlit_lottie import st_lottie
import requests

# Load environment variables
load_dotenv()

# Function to load Lottie animations
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Auto-refresh every 60 seconds
st_autorefresh(interval=60000, key="main_refresh")

# Page settings
st.set_page_config(page_title="TrendSeer", layout="wide")

# Google Fonts
st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap" rel="stylesheet">
    """,
    unsafe_allow_html=True
)

# Load custom CSS
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Page Title with Animation
st.title("TrendVision – Clear visibility into emerging digital trends")
st.caption("Real-time social listening: Reddit + optional news · NLP · Forecast")

# Lottie Animation (AI theme)
lottie_ai = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_jcikwtux.json")
st_lottie(lottie_ai, height=200)

# Load data safely
if os.path.exists("data/reddit_posts.csv"):
    df = pd.read_csv("data/reddit_posts.csv")
    df['sentiment'] = pd.to_numeric(df.get('sentiment', 0), errors='coerce').fillna(0)
    if 'date' not in df.columns and 'created_utc' in df.columns:
        df['date'] = pd.to_datetime(df['created_utc'], unit='s').dt.date
else:
    st.error("Run the pipeline first: python app.py -> python nlp/keywords.py -> python nlp/sentiment.py -> python forecast/forecast.py")
    st.stop()

# KPI Cards
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total posts", int(df.shape[0]))
c2.metric("Avg sentiment", round(df['sentiment'].mean(), 3))
c3.metric("Top keyword", df['keyword'].mode().iat[0] if 'keyword' in df.columns and not df['keyword'].isna().all() else "N/A")
c4.metric("Last update", str(df['date'].max() if 'date' in df.columns else 'N/A'))

# Instructions
st.markdown("Use the left sidebar (Pages) to open **Overview**, **Keyword Analysis**, **Forecast**, **Settings**.")
st.markdown("---")
st.write(
    "💡 **Tip:** Run `python app.py` to refresh raw data, then "
    "`python nlp/keywords.py` and `python nlp/sentiment.py`, "
    "then `python forecast/forecast.py`. Or use **Settings → Run Pipeline**."
)
