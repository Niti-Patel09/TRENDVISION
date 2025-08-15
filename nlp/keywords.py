# nlp/keywords.py — Extract keywords with KeyBERT (light)
from keybert import KeyBERT
import pandas as pd
import os

os.makedirs("data", exist_ok=True)
path = "data/reddit_posts.csv"
if not os.path.exists(path):
    raise SystemExit("data/reddit_posts.csv not found. Run app.py first.")

df = pd.read_csv(path)
df['title'] = df['title'].fillna("").astype(str)

kw_model = KeyBERT()  # uses sentence-transformers under the hood (ensure installed)
def top_keyword(text):
    try:
        res = kw_model.extract_keywords(text, keyphrase_ngram_range=(1,2), stop_words='english', top_n=1, use_mmr=True)
        return res[0][0] if res else ""
    except Exception as e:
        # fail-safe
        return ""

df['keyword'] = df['title'].apply(top_keyword)
df.to_csv(path, index=False)
print("✅ Keywords extracted and saved to data/reddit_posts.csv")
