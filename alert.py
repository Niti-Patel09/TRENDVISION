# alerts.py — detect spikes and send Slack messages
import os, pandas as pd
from dotenv import load_dotenv
load_dotenv()
SLACK_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_CHANNEL = os.getenv("SLACK_CHANNEL", "#general")

def send_slack_alert(message):
    if not SLACK_TOKEN:
        print("Slack token not set; skipping alert.")
        return
    from slack_sdk import WebClient
    client = WebClient(token=SLACK_TOKEN)
    try:
        client.chat_postMessage(channel=SLACK_CHANNEL, text=message)
        print("Slack alert sent.")
    except Exception as e:
        print("Slack send error:", e)

def check_for_spikes(multiplier=3):
    p = "data/reddit_posts.csv"
    if not os.path.exists(p):
        print("No reddit_posts.csv; skipping spikes check.")
        return
    df = pd.read_csv(p)
    if df.empty or 'created_utc' not in df.columns:
        return
    df['date'] = pd.to_datetime(df['created_utc'], unit='s').dt.date
    counts = df.groupby('date').size().sort_index()
    if len(counts) < 2:
        return
    latest = counts.iloc[-1]
    baseline = counts.iloc[:-1].tail(7).mean() if len(counts) > 1 else 0
    if baseline > 0 and latest > baseline * multiplier:
        top_kw = df['keyword'].value_counts().idxmax() if 'keyword' in df.columns and not df['keyword'].isna().all() else "N/A"
        send_slack_alert(f"🚀 Spike detected: {latest} posts today (baseline {baseline:.1f}). Top keyword: {top_kw}")

if __name__ == "__main__":
    check_for_spikes()
