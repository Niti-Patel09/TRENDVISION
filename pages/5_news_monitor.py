# pages/5_news_monitor.py
import streamlit as st
import pandas as pd
import feedparser
import os

# Page settings - Must be first Streamlit command
st.set_page_config(page_title="TrendVision AI - News", layout="wide", initial_sidebar_state="expanded")

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

st.title("📰 Global News Monitor")
st.markdown("### Connect Reddit Trends to Real-World Events")

if not os.path.exists("data/reddit_posts.csv"):
    st.warning("No data found. Please run the pipeline first.")
    st.stop()

df = pd.read_csv("data/reddit_posts.csv")

if 'keyword' not in df.columns:
    st.warning("Keywords not extracted yet. Run the pipeline.")
    st.stop()

# Get top keywords
top_keywords = df['keyword'].value_counts().head(10).index.tolist()

if not top_keywords:
    st.info("No keywords found to search for.")
    st.stop()

col1, col2 = st.columns([1, 3])

with col1:
    st.markdown("**Select a Trend:**")
    selected_kw = st.radio("Trending Topics", top_keywords)

with col2:
    st.subheader(f"Latest News: {selected_kw.title()}")
    
    # Fetch Google News RSS
    rss_url = f"https://news.google.com/rss/search?q={selected_kw.replace(' ', '+')}&hl=en-US&gl=US&ceid=US:en"
    feed = feedparser.parse(rss_url)
    
    if not feed.entries:
        st.info("No recent news found for this topic.")
    
    for entry in feed.entries[:8]:
        with st.container():
            st.markdown(f"#### [{entry.title}]({entry.link})")
            st.caption(f"📅 {entry.published} | 🔗 {entry.source.title}")
            st.markdown("---")