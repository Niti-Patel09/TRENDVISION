# pages/1_overview.py
import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import io, os

# Always load CSS from project root
css_path = os.path.join(os.path.dirname(__file__), "styles.css")
if not os.path.exists(css_path):  # fallback if script is in /pages/
    css_path = os.path.join(os.path.dirname(__file__), "..", "styles.css")

with open(css_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("📊 Market Overview")
st.markdown("### Top Keywords & Sentiment Analysis")

if not os.path.exists("data/reddit_posts.csv"):
    st.warning("No data found. Run the pipeline.")
    st.stop()

df = pd.read_csv("data/reddit_posts.csv")
if 'sentiment' not in df.columns:
    df['sentiment'] = 0
else:
    df['sentiment'] = pd.to_numeric(df['sentiment'], errors='coerce').fillna(0)
if 'date' not in df.columns and 'created_utc' in df.columns:
    df['date'] = pd.to_datetime(df['created_utc'], unit='s').dt.date

col_left, col_right = st.columns([3, 2])

if 'keyword' in df.columns:
    with col_left:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        topk = df['keyword'].value_counts().head(10).reset_index()
        topk.columns = ['keyword','count']
        fig = px.bar(topk, x='keyword', y='count', color='count', 
                     color_continuous_scale=['#00BFA6','#7C3AED'],
                     title="🔥 Trending Keywords")
        fig.update_layout(xaxis_tickangle=-45, margin=dict(t=50, b=0), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#fafafa')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("Keywords not yet extracted. Run 'nlp/keywords.py' or use Settings.")

with col_right:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 🎭 Sentiment Distribution")
    fig2 = px.histogram(df, x='sentiment', nbins=20, color_discrete_sequence=['#7C3AED'])
    fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#fafafa', height=350)
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="glass-card" style="margin-top:20px;">', unsafe_allow_html=True)
st.markdown("### ☁️ Visual Trend Cloud")
if 'keyword' in df.columns:
    text = " ".join(df['keyword'].dropna().astype(str))
    if text.strip():
        wc = WordCloud(width=800, height=350, background_color='black', colormap='cool', mode='RGBA').generate(text)
        st.image(wc.to_image(), use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)
