# pages/2_keyword_analysis.py
import streamlit as st
import pandas as pd
import plotly.express as px
from st_aggrid import AgGrid, GridOptionsBuilder
import os

# Page settings - Must be first Streamlit command
st.set_page_config(page_title="TrendVision AI - Analysis", layout="wide", initial_sidebar_state="expanded")

# Always load CSS from project root
css_path = os.path.join(os.path.dirname(__file__), "styles.css")
if not os.path.exists(css_path):  # fallback if script is in /pages/
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


st.title("🔍 Keyword Deep Dive")
if not os.path.exists("data/reddit_posts.csv"):
    st.warning("No data found.")
    st.stop()

df = pd.read_csv("data/reddit_posts.csv")
if 'sentiment' not in df.columns:
    df['sentiment'] = 0
else:
    df['sentiment'] = pd.to_numeric(df['sentiment'], errors='coerce').fillna(0)

df['created_utc'] = pd.to_numeric(df['created_utc'], errors='coerce')
df['date'] = pd.to_datetime(df['created_utc'], unit='s').dt.date

if 'keyword' not in df.columns:
    st.warning("Keywords not found in data. Please run the pipeline via Settings.")
    st.stop()

df['keyword'] = df['keyword'].astype(str).replace('nan', '')
kw_list = sorted([k for k in df['keyword'].unique() if k.strip()])

selected = st.selectbox("Select keyword", ["(all)"]+kw_list)
shown = df if selected=="(all)" else df[df['keyword']==selected]

st.markdown("### 📋 Raw Data Explorer")
gb = GridOptionsBuilder.from_dataframe(shown[['date','title','keyword','score','sentiment']])
gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=10)
gb.configure_default_column(groupable=True, sortable=True, filter=True)
gb.configure_column("sentiment", type=["numericColumn","numberColumnFilter"], precision=2)
AgGrid(shown[['date','title','keyword','score','sentiment']], gridOptions=gb.build(), height=350)

st.subheader(f"Sentiment Distribution: {selected}")
if not shown.empty:
    fig = px.histogram(shown, x='sentiment', nbins=25, color_discrete_sequence=['#00BFA6'], marginal="box")
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#fafafa', bargap=0.1)
    st.plotly_chart(fig, use_container_width=True)

# Compare two keywords section
st.markdown("---")
st.markdown("### ⚔️ Keyword Comparison")

if len(kw_list) >= 2:
    c1, c2 = st.columns(2)
    with c1:
        a = st.selectbox("Keyword A", kw_list, index=0, key="comp_a")
    with c2:
        b = st.selectbox("Keyword B", kw_list, index=1, key="comp_b")
    
    if a and b:
        cmp_df = df[df['keyword'].isin([a,b])].copy()
        
        # Metrics
        m1, m2, m3, m4 = st.columns(4)
        df_a = cmp_df[cmp_df['keyword']==a]
        df_b = cmp_df[cmp_df['keyword']==b]
        
        with m1: st.markdown('<div class="glass-card">', unsafe_allow_html=True); st.metric(f"{a} Vol", len(df_a)); st.markdown('</div>', unsafe_allow_html=True)
        with m2: st.markdown('<div class="glass-card">', unsafe_allow_html=True); st.metric(f"{a} Sent", f"{df_a['sentiment'].mean():.2f}"); st.markdown('</div>', unsafe_allow_html=True)
        with m3: st.markdown('<div class="glass-card">', unsafe_allow_html=True); st.metric(f"{b} Vol", len(df_b)); st.markdown('</div>', unsafe_allow_html=True)
        with m4: st.markdown('<div class="glass-card">', unsafe_allow_html=True); st.metric(f"{b} Sent", f"{df_b['sentiment'].mean():.2f}"); st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("#### ❤️ Sentiment Comparison")
        fig_box = px.box(cmp_df, x='keyword', y='sentiment', color='keyword', 
                         color_discrete_map={a: '#00BFA6', b: '#7C3AED'})
        fig_box.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#fafafa')
        st.plotly_chart(fig_box, use_container_width=True)

        st.markdown("#### 📈 Volume Trends")
        cmp_agg = cmp_df.groupby(['date','keyword']).size().reset_index(name='count')
        if not cmp_agg.empty:
            fig2 = px.line(cmp_agg, x='date', y='count', color='keyword', markers=True, 
                           color_discrete_map={a: '#00BFA6', b: '#7C3AED'})
            fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#fafafa')
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("Not enough data to display trend comparison.")
            
        st.markdown("---")
        st.markdown("### 🔬 Advanced Comparison Metrics")
        
        col_adv1, col_adv2 = st.columns(2)
        
        with col_adv1:
            st.markdown("#### 💠 Engagement vs. Sentiment")
            st.caption("Do positive or negative posts get more upvotes?")
            cmp_df['num_comments'] = cmp_df['num_comments'].fillna(0)
            fig_scatter = px.scatter(cmp_df, x='sentiment', y='score', color='keyword', 
                                     size='num_comments', hover_data=['title'],
                                     color_discrete_map={a: '#00BFA6', b: '#7C3AED'},
                                     labels={'score': 'Upvotes', 'sentiment': 'Sentiment Score'},
                                     opacity=0.8)
            fig_scatter.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#fafafa')
            st.plotly_chart(fig_scatter, use_container_width=True)
            
        with col_adv2:
            st.markdown("#### 📊 Average Engagement")
            st.caption("Comparing average Upvotes and Comments.")
            avg_metrics = cmp_df.groupby('keyword')[['score', 'num_comments']].mean().reset_index()
            avg_melt = avg_metrics.melt(id_vars='keyword', var_name='Metric', value_name='Value')
            
            fig_bar = px.bar(avg_melt, x='Metric', y='Value', color='keyword', barmode='group',
                             color_discrete_map={a: '#00BFA6', b: '#7C3AED'})
            fig_bar.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#fafafa')
            st.plotly_chart(fig_bar, use_container_width=True)
else:
    st.info("Need at least 2 keywords to enable comparison.")
