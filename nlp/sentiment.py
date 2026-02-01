# nlp/sentiment.py
import os, time, sys
import pandas as pd
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()

USE_TRANSFORMER = os.getenv("USE_TRANSFORMER", "false").lower() in ("1","true","yes")

try:
    from textblob import TextBlob
except Exception:
    TextBlob = None

if USE_TRANSFORMER:
    from transformers import pipeline
    _pipe = None
    def get_pipe():
        global _pipe
        if _pipe is None:
            _pipe = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
        return _pipe
    def transformer_sent(text):
        try:
            pipe = get_pipe()
            out = pipe(text[:512])[0]
            score = float(out.get("score",0.0))
            return score if out.get("label","")=="POSITIVE" else -score
        except:
            return 0.0

def textblob_sent(text):
    if not TextBlob or not text:
        return 0.0
    try:
        return float(TextBlob(str(text)).sentiment.polarity)
    except:
        return 0.0

path = "data/reddit_posts.csv"
if not os.path.exists(path):
    raise SystemExit("data/reddit_posts.csv missing. Run app.py")

df = pd.read_csv(path)
df['title'] = df['title'].fillna("").astype(str)

df['sentiment_light'] = df['title'].apply(textblob_sent)
if USE_TRANSFORMER:
    df['sentiment_transformer'] = df['title'].apply(transformer_sent)
    df['sentiment'] = df['sentiment_transformer'].fillna(df['sentiment_light'])
else:
    df['sentiment'] = df['sentiment_light']

df.to_csv(path, index=False)
print("✅ Sentiment added to data/reddit_posts.csv")
