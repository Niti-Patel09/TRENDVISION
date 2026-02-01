# app.py — Main data ingestion script (Reddit Scraper)
import praw
import pandas as pd
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "TrendVision/1.0")
SUBREDDITS = os.getenv("SUBREDDITS", "technology").split("+")

def fetch_reddit_data():
    print("🚀 Starting Reddit data fetch...")
    
    if not REDDIT_CLIENT_ID or not REDDIT_CLIENT_SECRET:
        sys.exit("❌ Error: Reddit API credentials (ID or Secret) are missing in .env file.")
    
    print(f"   Using User-Agent: {REDDIT_USER_AGENT}")

    try:
        reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent=REDDIT_USER_AGENT
        )
    except Exception as e:
        print(f"❌ Error initializing Reddit client: {e}")
        return

    all_posts = []
    for sub in SUBREDDITS:
        print(f"   Scanning r/{sub}...")
        try:
            subreddit = reddit.subreddit(sub)
            # Fetch Hot and New posts
            limit = 50
            for post in subreddit.hot(limit=limit):
                all_posts.append(process_post(post, sub))
            for post in subreddit.new(limit=limit):
                all_posts.append(process_post(post, sub))
        except Exception as e:
            print(f"   ⚠️ Could not fetch r/{sub}: {e}")
            if "401" in str(e):
                print("      👉 Tip: 401 means 'Unauthorized'. Check your Client ID and Secret.")

    if not all_posts:
        print("⚠️ No posts found. Check your internet connection or API credentials.")
        return

    df = pd.DataFrame(all_posts)
    df = df.drop_duplicates(subset=['id'])
    
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/reddit_posts.csv", index=False)
    print(f"✅ Saved {len(df)} unique posts to data/reddit_posts.csv")

def process_post(post, sub):
    return {
        "id": post.id,
        "title": post.title,
        "score": post.score,
        "url": post.url,
        "num_comments": post.num_comments,
        "created_utc": post.created_utc,
        "selftext": post.selftext,
        "subreddit": sub
    }

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8')
    fetch_reddit_data()