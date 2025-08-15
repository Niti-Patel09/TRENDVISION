# pages/3_forecast.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

# Always load CSS from project root
css_path = os.path.join(os.path.dirname(__file__), "styles.css")
if not os.path.exists(css_path):  # fallback if script is in /pages/
    css_path = os.path.join(os.path.dirname(__file__), "..", "styles.css")

with open(css_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


st.header("Forecast")
if not os.path.exists("data/forecast.csv"):
    st.warning("Forecast not found. Run forecast/forecast.py")
    st.stop()

forecast = pd.read_csv("data/forecast.csv")
forecast['ds'] = pd.to_datetime(forecast['ds'])
fig = go.Figure()
fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], mode='lines', name='yhat'))
if 'yhat_lower' in forecast.columns and 'yhat_upper' in forecast.columns:
    fig.add_trace(go.Scatter(
        x=list(forecast['ds']) + list(forecast['ds'][::-1]),
        y=list(forecast['yhat_upper']) + list(forecast['yhat_lower'][::-1]),
        fill='toself', fillcolor='rgba(0,176,246,0.2)', line=dict(color='rgba(255,255,255,0)'), showlegend=False
    ))
fig.update_layout(title="Forecasted Post Volume", xaxis_title="Date", yaxis_title="Count")
st.plotly_chart(fig, use_container_width=True)
st.download_button("⬇ Download forecast.csv", forecast.to_csv(index=False).encode('utf-8'), file_name="forecast.csv")
