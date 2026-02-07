# pages/3_forecast.py
import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Page settings - Must be first Streamlit command
st.set_page_config(page_title="TrendVision AI - Forecast", layout="wide", initial_sidebar_state="expanded")

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

st.title("🔮 AI Trend Forecast")

if not os.path.exists("data/forecast.csv"):
    st.warning("No forecast data found. Please run the pipeline via Settings.")
    st.stop()

df = pd.read_csv("data/forecast.csv")
# Prophet outputs 'ds' as date string, 'yhat' as value

if df.empty:
    st.warning("Forecast data is empty. Try running the pipeline again.")
    st.stop()

df['ds'] = pd.to_datetime(df['ds'])

st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown("### 📈 AI Post Volume Forecast")
st.caption("Predicting community engagement for the next 7 days using Prophet AI.")

fig = px.line(df, x='ds', y='yhat', markers=True)
fig.update_traces(line_color='#8B5CF6', line_width=4, marker=dict(size=10, color='#10B981', line=dict(width=2, color='white')))
fig.update_layout(xaxis_title="", yaxis_title="Predicted Posts", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#fafafa', height=450)
st.plotly_chart(fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

with st.expander("View Raw Forecast Data"):
    st.dataframe(df)