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


st.header("Overview — Top Keywords & Sentiment")
if not os.path.exists("data/reddit_posts.csv"):
    st.warning("No data found. Run the pipeline.")
    st.stop()

df = pd.read_csv("data/reddit_posts.csv")
df['sentiment'] = pd.to_numeric(df.get('sentiment',0), errors='coerce').fillna(0)
if 'date' not in df.columns and 'created_utc' in df.columns:
    df['date'] = pd.to_datetime(df['created_utc'], unit='s').dt.date

topk = df['keyword'].value_counts().head(15).reset_index()
topk.columns = ['keyword','count']
fig = px.bar(topk, x='keyword', y='count', color='count', color_continuous_scale=['#00BFA6','#7C3AED'])
fig.update_layout(xaxis_tickangle=-45, margin=dict(t=50))
st.plotly_chart(fig, use_container_width=True)

st.subheader("Sentiment distribution")
fig2 = px.histogram(df, x='sentiment', nbins=30)
st.plotly_chart(fig2, use_container_width=True)

st.subheader("Word cloud (keywords)")
wc = WordCloud(width=800, height=350, background_color=None, mode='RGBA').generate(" ".join(df['keyword'].dropna()))
buf = io.BytesIO(); wc.save(buf, format="PNG")
st.image(buf.getvalue(), use_column_width=True)
