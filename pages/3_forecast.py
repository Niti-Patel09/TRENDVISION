# pages/3_forecast.py
import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Load CSS
css_path = os.path.join(os.path.dirname(__file__), "..", "styles.css")
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

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
st.plotly_chart(fig, width='stretch')
st.markdown('</div>', unsafe_allow_html=True)

with st.expander("View Raw Forecast Data"):
    st.dataframe(df)