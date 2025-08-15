# data_source.py (optional): fetch news headlines (NewsAPI)
import os, requests, pandas as pd
from dotenv import load_dotenv
load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
if not NEWS_API_KEY:
    print("No NEWS_API_KEY; skipping news fetch.")
else:
    q = "technology"
    url = f"https://newsapi.org/v2/everything?q={q}&sortBy=publishedAt&pageSize=100&apiKey={NEWS_API_KEY}"
    r = requests.get(url)
    if r.status_code == 200:
        items = r.json().get("articles", [])
        rows = [{"title": a["title"], "source": a["source"]["name"], "publishedAt": a["publishedAt"]} for a in items]
        pd.DataFrame(rows).to_csv("data/news.csv", index=False)
        print("✅ news.csv saved.")
    else:
        print("NewsAPI fetch failed:", r.status_code, r.text)
