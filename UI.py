# ui.py — root home page (lightweight nav & shared data)
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import plotly.express as px
import plotly.graph_objects as go
import os
from streamlit_autorefresh import st_autorefresh
from streamlit_lottie import st_lottie
import requests
import sys
import subprocess
import time

# Load environment variables
load_dotenv()

# Function to load Lottie animations
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Page settings
st.set_page_config(page_title="TrendVision", layout="wide")

# Auto-refresh every 60 seconds
st_autorefresh(interval=60000, key="main_refresh")

# Google Fonts
st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    """,
    unsafe_allow_html=True
)

# Load custom CSS
css_path = os.path.join(os.path.dirname(__file__), "styles.css")
with open(css_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Hero Section
col_hero_1, col_hero_2 = st.columns([2, 1])
with col_hero_1:
    st.title("TrendVision AI")
    st.markdown("### ⚡ Real-time Social Intelligence")
    st.markdown("Analyze Reddit trends, detect emerging keywords, and forecast future engagement using advanced NLP.")
with col_hero_2:
    lottie_ai = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_jcikwtux.json")
    if lottie_ai:
        st_lottie(lottie_ai, height=180)

# Load data safely
if os.path.exists("data/reddit_posts.csv"):
    df = pd.read_csv("data/reddit_posts.csv")
    if 'sentiment' not in df.columns:
        df['sentiment'] = 0
    else:
        df['sentiment'] = pd.to_numeric(df['sentiment'], errors='coerce').fillna(0)
    if 'date' not in df.columns and 'created_utc' in df.columns:
        df['date'] = pd.to_datetime(df['created_utc'], unit='s').dt.date
else:
    st.info("👋 Welcome! Let's initialize your data pipeline to get started.")
    
    if st.button("🚀 Initialize System & Fetch Data", type="primary"):
        with st.spinner("Running pipeline... (This may take a minute)"):
            # 1. Fetch Data
            result = subprocess.run([sys.executable, "app.py"], capture_output=True, text=True)
            
            if not os.path.exists("data/reddit_posts.csv"):
                st.error("❌ Data fetch failed. Please check your .env file for valid Reddit credentials.")
                st.markdown("### Error Log:")
                stdout = result.stdout if result.stdout else ""
                stderr = result.stderr if result.stderr else ""
                st.code(stdout + "\n" + stderr)
                st.stop()

            # 2. NLP & Forecast
            subprocess.run([sys.executable, "nlp/keywords.py"])
            subprocess.run([sys.executable, "nlp/sentiment.py"])
            subprocess.run([sys.executable, "forecast/forecast.py"])
        st.success("Pipeline finished! Reloading...")
        time.sleep(2)
        st.rerun()

    st.stop()

# AI-Powered Smart UI Logic
avg_sent = df['sentiment'].mean()
total_vol = len(df)

def get_ai_briefing(sentiment, volume):
    if volume < 10: return "System warming up. Fetch more data for deep insights."
    if sentiment > 0.2: return "🚀 Market sentiment is highly bullish. Community engagement is positive."
    if sentiment < -0.2: return "⚠️ Caution: Negative sentiment spike detected. Potential controversy brewing."
    return "⚖️ Stable trends. Consistent engagement across monitored subreddits."

def get_smart_recommendation(df):
    top_sub = df['subreddit'].mode().iat[0] if 'subreddit' in df.columns else "N/A"
    if df['sentiment'].mean() < 0:
        return f"🔍 **Deep Dive Needed**: Sentiment in r/{top_sub} is dropping. Check 'Keyword Analysis'."
    return f"🚀 **Growth Opportunity**: r/{top_sub} is showing high engagement. Check 'AI Forecast'."

# KPI Cards
st.markdown(f"""
    <div style="display: flex; gap: 20px; margin-bottom: 25px;">
        <div class="ai-insight-box" style="flex: 2;">
            <h4 style="margin:0; color:#8B5CF6;">✨ AI Daily Briefing</h4>
            <p style="margin:5px 0 0 0; font-size:1.1rem; opacity:0.9;">{get_ai_briefing(avg_sent, total_vol)}</p>
        </div>
        <div class="glass-card" style="flex: 1; padding: 15px; border-color: var(--secondary);">
            <h5 style="margin:0; color:var(--secondary);">💡 Next Best Action</h5>
            <p style="margin:5px 0 0 0; font-size:0.9rem;">{get_smart_recommendation(df)}</p>
        </div>
    </div>
""", unsafe_allow_html=True)

st.write("")

st.write("")
c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown('<div class="glass-card">', unsafe_allow_html=True); st.metric("Total Posts", int(df.shape[0])); st.markdown('</div>', unsafe_allow_html=True)
with c2: st.markdown('<div class="glass-card">', unsafe_allow_html=True); st.metric("Avg Sentiment", round(avg_sent, 3)); st.markdown('</div>', unsafe_allow_html=True)
with c3: 
    top_kw = df['keyword'].mode().iat[0] if 'keyword' in df.columns and not df['keyword'].isna().all() else "N/A"
    st.markdown('<div class="glass-card">', unsafe_allow_html=True); st.metric("Top Keyword", top_kw); st.markdown('</div>', unsafe_allow_html=True)
with c4: st.markdown('<div class="glass-card">', unsafe_allow_html=True); st.metric("Last Update", str(df['date'].max() if 'date' in df.columns else 'N/A')); st.markdown('</div>', unsafe_allow_html=True)

# Dashboard Widgets
st.markdown("---")

col_dash_1, col_dash_2 = st.columns([1, 2])

with col_dash_1:
    # Global Sentiment Gauge
    avg_sentiment = df['sentiment'].mean()
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = avg_sentiment,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Global Sentiment Score", 'font': {'size': 20, 'color': '#fafafa'}},
        gauge = {
            'axis': {'range': [-1, 1], 'tickwidth': 1, 'tickcolor': "white"},
            'bar': {'color': "#7C3AED"},
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 2,
            'bordercolor': "#374151",
            'steps': [
                {'range': [-1, -0.3], 'color': "rgba(239, 68, 68, 0.3)"},
                {'range': [-0.3, 0.3], 'color': "rgba(55, 65, 81, 0.3)"},
                {'range': [0.3, 1], 'color': "rgba(16, 185, 129, 0.3)"}],
        }
    ))
    fig_gauge.update_layout(paper_bgcolor = "rgba(0,0,0,0)", font = {'color': "white", 'family': "Inter"}, height=300, margin=dict(l=20, r=20, t=50, b=20))
    st.plotly_chart(fig_gauge, use_container_width=True)

with col_dash_2:
    # Activity Trend
    daily_counts = df.groupby('date').size().reset_index(name='counts')
    fig_trend = px.area(daily_counts, x='date', y='counts', title="📈 Activity Volume Trend", color_discrete_sequence=['#00BFA6'])
    fig_trend.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#fafafa', height=300)
    st.plotly_chart(fig_trend, use_container_width=True)

st.markdown("### 📡 Recent Signals")
st.dataframe(df[['date', 'title', 'subreddit', 'score', 'sentiment']].sort_values(by='date', ascending=False).head(10), use_container_width=True)

# Instructions
st.markdown("### 🧭 Navigation")
col_nav1, col_nav2, col_nav3, col_nav4 = st.columns(4)
with col_nav1:
    st.info("**📊 Overview**: High-level insights and sentiment distribution.")
with col_nav2:
    st.info("**🔍 Deep Dive**: Analyze specific keywords and compare trends.")
with col_nav3:
    st.info("**📰 News Monitor**: Real-time external news context.")
with col_nav4:
    st.info("**⚔️ Comparison**: Benchmark different subreddits.")
