# pages/5_news_monitor.py
import streamlit as st
import pandas as pd
import feedparser
import os

# Load CSS
css_path = os.path.join(os.path.dirname(__file__), "..", "styles.css")
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

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