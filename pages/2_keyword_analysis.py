# pages/2_keyword_analysis.py
import streamlit as st
import pandas as pd
import plotly.express as px
from st_aggrid import AgGrid, GridOptionsBuilder
import os

# Always load CSS from project root
css_path = os.path.join(os.path.dirname(__file__), "styles.css")
if not os.path.exists(css_path):  # fallback if script is in /pages/
    css_path = os.path.join(os.path.dirname(__file__), "..", "styles.css")

with open(css_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


st.header("Keyword Analysis")
if not os.path.exists("data/reddit_posts.csv"):
    st.warning("No data found.")
    st.stop()

df = pd.read_csv("data/reddit_posts.csv")
df['sentiment'] = pd.to_numeric(df.get('sentiment',0), errors='coerce').fillna(0)
if 'date' not in df.columns and 'created_utc' in df.columns:
    df['date'] = pd.to_datetime(df['created_utc'], unit='s').dt.date

kw_list = df['keyword'].dropna().unique().tolist()
selected = st.selectbox("Select keyword", ["(all)"]+kw_list)
shown = df if selected=="(all)" else df[df['keyword']==selected]

gb = GridOptionsBuilder.from_dataframe(shown[['date','title','keyword','score','sentiment']])
gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=10)
gb.configure_default_column(groupable=True, sortable=True, filter=True)
AgGrid(shown[['date','title','keyword','score','sentiment']], gridOptions=gb.build(), height=350)

st.subheader(f"Sentiment for: {selected}")
fig = px.histogram(shown, x='sentiment', nbins=25)
st.plotly_chart(fig, use_container_width=True)

# Compare two keywords section
st.subheader("Compare two keywords")
if len(kw_list) >= 2:
    a = st.selectbox("Keyword A", kw_list, key="comp_a")
    b = st.selectbox("Keyword B", kw_list, key="comp_b")
    cmp_df = df[df['keyword'].isin([a,b])]
    cmp_agg = cmp_df.groupby(['date','keyword']).size().reset_index(name='count')
    fig2 = px.line(cmp_agg, x='date', y='count', color='keyword')
    st.plotly_chart(fig2, use_container_width=True)
