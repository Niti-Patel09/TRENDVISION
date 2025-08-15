# TRENDVISION

# **TrendVision**  
_Real-Time Social Listening & Predictive Trend Analytics Platform_  

---

## 📌 Overview  

**TrendVision** is a **real-time social media monitoring and predictive analytics platform** that tracks discussions across platforms like **Reddit** (and optionally news sources) to:  

- Monitor **emerging trends** before they go mainstream  
- Analyze **public sentiment** using advanced **NLP & AI models**  
- Visualize **topic popularity and engagement over time**  
- Forecast **future trends** with machine learning  
- Provide **actionable insights** for brands, marketers, and analysts  

---

## 🎯 Problem Statement  

In today’s digital-first world, **information spreads faster than ever**. Brands, investors, and researchers need to detect emerging trends **before competitors do**.  

**Challenges**:  
- Social media data is **unstructured and noisy**  
- Identifying **true signals** from the noise is difficult  
- Understanding **public sentiment** requires advanced NLP  
- Manual monitoring is **time-consuming and incomplete**  

**TrendVision** solves this by **automating trend detection, sentiment analysis, and forecasting** in one platform.  

---

## 🚀 Key Features  

- **Real-Time Data Collection** from Reddit & optional news sources  
- **Sentiment Analysis** using VADER & Transformers  
- **Keyword Extraction** & Topic Clustering with BERTopic  
- **Trend Forecasting** using Facebook Prophet / ARIMA  
- **Multi-Page Interactive Dashboard** with Streamlit  
- **Slack Integration** for automated trend reports  

---

## 🛠️ Tech Stack  

| Layer              | Technology |
|--------------------|------------|
| **Frontend**       | Streamlit, CSS custom theming |
| **Backend**        | Python 3.11+ |
| **Data Collection**| Reddit API (PRAW), NewsAPI |
| **Data Processing**| Pandas, NumPy |
| **NLP**            | Transformers, VADER, NLTK, SentenceTransformers |
| **Topic Modeling** | BERTopic, UMAP, HDBSCAN, Gensim |
| **Forecasting**    | Prophet, ARIMA |
| **Visualization**  | Plotly, Matplotlib, WordCloud |
| **Integration**    | Slack SDK, Python-Dotenv |
| **Deployment**     | Streamlit Cloud / Docker / Local |

---

## 📂 Project Structure  

```

TrendVision/
│── app.py                  # Main data collection script
│── ui.py                   # Homepage dashboard
│── styles.css              # Global CSS theme
│── requirements.txt        # Python dependencies
│── .env                    # API keys and config (local only)
│
├── pages/                  # Streamlit pages
│   ├── 1\_📊\_Overview\.py
│   ├── 2\_🔍\_Keyword\_Analysis.py
│   ├── 3\_🔮\_Forecast.py
│   ├── 4\_⚙️\_Settings.py
│
├── data/                   # Saved datasets
│   ├── reddit\_posts.csv
│   ├── sentiment.csv
│
├── nlp/                    # NLP processing
│   ├── keywords.py
│   ├── sentiment.py
│
└── forecast/               # Forecasting scripts
├── forecast.py

````

---

## ⚙️ Installation & Setup  

### 1️⃣ Clone the Repository  
```bash
git clone https://github.com/yourusername/trendvision.git
cd trendvision
````

### 2️⃣ Create Virtual Environment & Install Dependencies

```bash
python -m venv venv
venv\Scripts\activate    # Windows
# or
source venv/bin/activate # Mac/Linux

pip install -r requirements.txt
```

### 3️⃣ Setup Environment Variables

Rename `.env.template` → `.env` and fill in:

```ini
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=trendvision:v1.0 (by /u/yourusername)
REDDIT_SUBREDDITS=technology,ai,news
REDDIT_LIMIT=200

NEWS_API_KEY=your_newsapi_key

SLACK_BOT_TOKEN=your_slack_token
SLACK_CHANNEL=#your-channel

USE_TRANSFORMER=false
USE_BERTOPIC=false
```

### 4️⃣ Run the Data Pipeline

```bash
python app.py
python nlp/keywords.py
python nlp/sentiment.py
python forecast/forecast.py
```

### 5️⃣ Launch the Dashboard

```bash
streamlit run ui.py
```

---

## 📊 Sample Output

* **Dashboard:** KPI cards, charts, forecasts
* **WordCloud:** Visual representation of trending topics
* **Forecast Graph:** Predicted popularity trends
* **Slack Report:** Automated insights in your channel

---

## 💡 Potential Use Cases

* **Brand Monitoring** – Track how people talk about your company
* **Crisis Detection** – Spot negative sentiment spikes early
* **Market Research** – Identify consumer interest shifts
* **Investment Intelligence** – Detect sectors gaining online buzz
* **Content Strategy** – Target trending topics for higher engagement

---

## 📈 Future Enhancements

* Add **Twitter / YouTube data collection**
* Enable **real-time streaming mode** with WebSockets
* Multi-language sentiment analysis
* Advanced **interactive visualizations** (D3.js integration)
* Export insights to **Excel / PDF / BI Tools**

---

## 📜 License

This project is licensed under the **MIT License** – free to use, modify, and distribute.

---




