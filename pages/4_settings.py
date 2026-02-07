# pages/4_settings.py
import streamlit as st
import subprocess
import sys
import os

# Page settings - Must be first Streamlit command
st.set_page_config(page_title="TrendVision AI - Settings", layout="wide", initial_sidebar_state="expanded")

# Load CSS
css_path = os.path.join(os.path.dirname(__file__), "..", "styles.css")
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Sidebar Branding
with st.sidebar:
    st.markdown("""
        <div style="padding: 10px; text-align: center;">
            <h2 style="color: #7C3AED; margin-bottom: 0;">TV AI</h2>
            <hr style="margin: 10px 0; border-color: rgba(255,255,255,0.1);">
        </div>
    """, unsafe_allow_html=True)

# Functional Top Navigation Bar
nav_cols = st.columns([1, 1, 1, 1, 1, 1, 1])
with nav_cols[0]: 
    if st.button("🏠 Home", use_container_width=True): st.switch_page("UI.py")
with nav_cols[1]: 
    if st.button("📊 Overview", use_container_width=True): st.switch_page("pages/1_overview.py")
with nav_cols[2]: 
    if st.button("🔍 Analysis", use_container_width=True): st.switch_page("pages/2_keyword_analysis.py")
with nav_cols[3]: 
    if st.button("🔮 Forecast", use_container_width=True): st.switch_page("pages/3_forecast.py")
with nav_cols[4]: 
    if st.button("📰 News", use_container_width=True): st.switch_page("pages/5_news_monitor.py")
with nav_cols[5]: 
    if st.button("⚔️ Compare", use_container_width=True): st.switch_page("pages/6_subreddit_comparison.py")
with nav_cols[6]: 
    if st.button("⚙️ Settings", use_container_width=True): st.switch_page("pages/4_settings.py")

st.title("⚙️ Control Panel")

st.info("Ensure your `.env` file is configured with Reddit API credentials before running the pipeline.")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🚀 Data Pipeline Control")

    if st.button("🔥 Run Full Pipeline (All Steps)", type="primary", use_container_width=True):
        with st.status("Executing full intelligence pipeline...", expanded=True) as status:
            st.write("1. Fetching Reddit data...")
            subprocess.run([sys.executable, "app.py"], check=True)
            st.write("2. Extracting semantic keywords...")
            subprocess.run([sys.executable, os.path.join("nlp", "keywords.py")], check=True)
            st.write("3. Analyzing sentiment patterns...")
            subprocess.run([sys.executable, os.path.join("nlp", "sentiment.py")], check=True)
            st.write("4. Generating predictive forecast...")
            subprocess.run([sys.executable, os.path.join("forecast", "forecast.py")], check=True)
            status.update(label="Pipeline Complete!", state="complete", expanded=False)
        st.success("System initialized successfully!")

    st.markdown("---")
    st.subheader("🛠️ Individual Steps")
    
    if st.button("1. Fetch Data (app.py)", use_container_width=True):
        with st.spinner("Fetching data from Reddit..."):
            res = subprocess.run([sys.executable, "app.py"], capture_output=True, text=True)
            if res.returncode == 0:
                st.success("Data fetched successfully!")
                with st.expander("View Logs"):
                    st.code(res.stdout)
            else:
                st.error("Error fetching data")
                st.code(res.stderr)

    if st.button("2. Extract Keywords (nlp/keywords.py)", use_container_width=True):
        with st.spinner("Extracting keywords (this may take a moment)..."):
            res = subprocess.run([sys.executable, os.path.join("nlp", "keywords.py")], capture_output=True, text=True)
            if res.returncode == 0:
                st.success("Keywords extracted!")
                with st.expander("View Logs"):
                    st.code(res.stdout)
            else:
                st.error("Extraction failed")
                st.code(res.stderr)

    if st.button("3. Analyze Sentiment (nlp/sentiment.py)", use_container_width=True):
        with st.spinner("Analyzing sentiment..."):
            res = subprocess.run([sys.executable, os.path.join("nlp", "sentiment.py")], capture_output=True, text=True)
            if res.returncode == 0:
                st.success("Sentiment analysis complete!")
                with st.expander("View Logs"):
                    st.code(res.stdout)
            else:
                st.error("Analysis failed")
                st.code(res.stderr)

    if st.button("4. Generate Forecast (forecast/forecast.py)", use_container_width=True):
        with st.spinner("Generating forecast..."):
            res = subprocess.run([sys.executable, os.path.join("forecast", "forecast.py")], capture_output=True, text=True)
            if res.returncode == 0:
                st.success("Forecast generated!")
                with st.expander("View Logs"):
                    st.code(res.stdout)
            else:
                st.error("Forecasting failed")
                st.code(res.stderr)

with col2:
    st.subheader("⚙️ Configuration")
    st.markdown("To update your API credentials or subreddit list, please edit the `.env` file in the project root directory directly for security reasons.")
    st.warning("The environment file is now hidden from the UI to protect your sensitive API keys.")