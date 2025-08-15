# topic_model.py (optional heavy) — run only if USE_BERTOPIC=true in .env
import os
from dotenv import load_dotenv
load_dotenv()
USE_BERTOPIC = os.getenv("USE_BERTOPIC","false").lower() in ("1","true","yes")
if not USE_BERTOPIC:
    print("BERTopic disabled (USE_BERTOPIC not set).")
    raise SystemExit

import pandas as pd
from bertopic import BERTopic

df = pd.read_csv("data/reddit_posts.csv")
texts = df['title'].fillna("").astype(str).tolist()
if len(texts) < 10:
    print("Not enough data for topic modelling.")
    raise SystemExit

topic_model = BERTopic(verbose=False)
topics, probs = topic_model.fit_transform(texts)
df['topic'] = topics
os.makedirs("data", exist_ok=True)
df.to_csv("data/reddit_posts_topics.csv", index=False)
os.makedirs("models", exist_ok=True)
topic_model.save("models/bertopic_model")
print("✅ Topics saved to data/reddit_posts_topics.csv and model saved.")
