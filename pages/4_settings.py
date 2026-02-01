# pages/4_settings.py
import streamlit as st
import subprocess
import sys
import os

# Load CSS
css_path = os.path.join(os.path.dirname(__file__), "..", "styles.css")
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("⚙️ Control Panel")

st.info("Ensure your `.env` file is configured with Reddit API credentials before running the pipeline.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Data Pipeline")
    
    if st.button("1. Fetch Data (app.py)", use_container_width=True):
        with st.spinner("Fetching data from Reddit..."):
            res = subprocess.run([sys.executable, "app.py"], capture_output=True, text=True)
            if res.returncode == 0:
                st.success("Data fetched successfully!")
                st.code(res.stdout)
            else:
                st.error("Error fetching data")
                st.code(res.stderr)

    if st.button("2. Extract Keywords (nlp/keywords.py)", use_container_width=True):
        with st.spinner("Extracting keywords (this may take a moment)..."):
            res = subprocess.run([sys.executable, "nlp/keywords.py"], capture_output=True, text=True)
            st.success("Keywords extracted!")
            st.code(res.stdout)

    if st.button("3. Analyze Sentiment (nlp/sentiment.py)", use_container_width=True):
        with st.spinner("Analyzing sentiment..."):
            res = subprocess.run([sys.executable, "nlp/sentiment.py"], capture_output=True, text=True)
            st.success("Sentiment analysis complete!")
            st.code(res.stdout)

    if st.button("4. Generate Forecast (forecast/forecast.py)", use_container_width=True):
        with st.spinner("Generating forecast..."):
            res = subprocess.run([sys.executable, "forecast/forecast.py"], capture_output=True, text=True)
            st.success("Forecast generated!")
            st.code(res.stdout)

with col2:
    st.subheader("Configuration")
    st.markdown("Edit the `.env` file in the project root to change settings.")
    st.code(open(".env").read() if os.path.exists(".env") else "No .env file found", language="bash")