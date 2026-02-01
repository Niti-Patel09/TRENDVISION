# pages/6_subreddit_comparison.py
import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Load CSS
css_path = os.path.join(os.path.dirname(__file__), "..", "styles.css")
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("⚔️ Community Intelligence")
st.markdown("### Compare Subreddit Performance & Sentiment")

if not os.path.exists("data/reddit_posts.csv"):
    st.warning("No data found. Please run the pipeline first.")
    st.stop()

df = pd.read_csv("data/reddit_posts.csv")

if 'subreddit' not in df.columns:
    st.error("Subreddit data missing.")
    st.stop()

# Aggregation
sub_stats = df.groupby('subreddit').agg({
    'id': 'count',
    'score': 'mean',
    'num_comments': 'mean',
    'sentiment': 'mean'
}).reset_index()

sub_stats.columns = ['Subreddit', 'Post Volume', 'Avg Score', 'Avg Comments', 'Avg Sentiment']

# Visuals
c1, c2 = st.columns(2)

with c1:
    st.markdown("#### 📢 Share of Voice (Volume)")
    fig1 = px.pie(sub_stats, values='Post Volume', names='Subreddit', hole=0.4, 
                  color_discrete_sequence=px.colors.sequential.Teal)
    fig1.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#fafafa')
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    st.markdown("#### ❤️ Sentiment by Community")
    fig2 = px.bar(sub_stats, x='Subreddit', y='Avg Sentiment', color='Avg Sentiment',
                  color_continuous_scale=['#EF4444', '#10B981'])
    fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#fafafa')
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("### 📋 Detailed Metrics")
st.dataframe(sub_stats.style.background_gradient(cmap="Purples", subset=['Avg Score', 'Avg Comments']), use_container_width=True)

st.info("💡 **Insight:** Higher sentiment indicates a more positive community reception. High volume with low sentiment might indicate controversy.")