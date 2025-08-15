# app.py — Reddit scraper (writes data/reddit_posts.csv)
import os, time
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "trendseer:v1 (by /u/unknown)")
SUBREDDITS = os.getenv("REDDIT_SUBREDDITS", "technology,ai").split(",")
LIMIT = int(os.getenv("REDDIT_LIMIT", "200"))

if not REDDIT_CLIENT_ID or not REDDIT_CLIENT_SECRET:
    raise RuntimeError("Missing REDDIT_CLIENT_ID/REDDIT_CLIENT_SECRET in .env")

import praw
reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID,
                     client_secret=REDDIT_CLIENT_SECRET,
                     user_agent=REDDIT_USER_AGENT)

posts = []
for sr in SUBREDDITS:
    sr = sr.strip()
    try:
        subreddit = reddit.subreddit(sr)
        for p in subreddit.hot(limit=LIMIT):
            posts.append({
                "id": getattr(p, "id", ""),
                "subreddit": sr,
                "title": getattr(p, "title", "")[:2000],
                "selftext": getattr(p, "selftext", "")[:4000],
                "created_utc": getattr(p, "created_utc", 0),
                "score": getattr(p, "score", 0),
                "num_comments": getattr(p, "num_comments", 0),
                "url": getattr(p, "url", ""),
                "author": str(getattr(p, "author", ""))[:100]
            })
    except Exception as e:
        print(f"Error scraping /r/{sr}: {e}")

df = pd.DataFrame(posts)
if df.empty:
    print("No posts fetched.")
else:
    # dedupe by id
    df = df.drop_duplicates(subset=["id"])
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/reddit_posts.csv", index=False)
    print(f"✅ Saved {len(df)} posts to data/reddit_posts.csv")
