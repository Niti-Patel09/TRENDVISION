# 🚀 TrendVision AI
**Real-Time Social Intelligence & Predictive Trend Analytics Platform**

TrendVision is a high-end analytical dashboard designed to bridge the gap between raw social chatter and actionable market intelligence. By combining **Glassmorphic UI/UX** with advanced **Transformer-based NLP** and **Time-Series Forecasting**, TrendVision allows users to detect emerging signals before they go mainstream.

---

## ✨ Key Features

### 🤖 1. AI-Powered UI & UX
- **Smart Personalization**: Adaptive interfaces that predict user intent based on data trends.
- **Contextual Briefings**: Dynamic AI-generated summaries that change based on real-time sentiment spikes.
- **Responsive Motion**: Purpose-driven micro-interactions and Lottie animations for a tactile, premium feel.

### 🧊 2. Modern Design Language
- **Glassmorphism**: Semi-transparent panels with backdrop-blur effects for visual depth.
- **Neumorphism**: Subtle shadows and highlights creating a sleek, futuristic mobile-friendly interface.
- **Interactive Visuals**: High-fidelity charts using Plotly and WordCloud for intuitive data exploration.

### 🧠 3. Advanced Analytics Pipeline
- **Keyword Extraction**: Powered by **KeyBERT** (Sentence-Transformers) for context-aware trend detection.
- **Sentiment Analysis**: Hybrid engine using **TextBlob** for speed and **DistilBERT** for deep semantic accuracy.
- **Predictive Forecasting**: Utilizes **Facebook Prophet** to model community engagement and predict future volume.
- **Topic Modeling**: Optional **BERTopic** integration for latent theme discovery.

### 📡 4. Multi-Channel Intelligence
- **Reddit Scraper**: Asynchronous ingestion via PRAW across multiple subreddits.
- **News Monitor**: Real-time RSS integration to correlate social trends with global news events.
- **Community Benchmarking**: Side-by-side comparison of subreddit performance and sentiment.

---

## 🛠️ Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Frontend** | Streamlit, Custom CSS (Glassmorphism), Lottie |
| **Data Ingestion** | PRAW (Reddit API), Feedparser (RSS) |
| **NLP** | KeyBERT, DistilBERT, TextBlob, BERTopic |
| **Forecasting** | Facebook Prophet |
| **Visualization** | Plotly, WordCloud, Streamlit-AgGrid |
| **Integration** | Slack SDK, Python-Dotenv |

---

## ⚙️ Installation & Setup

### 1. Clone & Install
```bash
git clone https://github.com/yourusername/trendvision.git
cd trendvision
pip install -r requirements.txt
```

### 2. Configure Reddit API
1. Visit Reddit App Preferences.
2. Scroll to the bottom and click **"are you a developer? create an app..."**.
3. **Name**: `TrendVision` | **Type**: `script` | **Redirect URI**: `http://localhost:8080`.
4. Copy your **Client ID** and **Secret** into the `.env` file.

### 3. Environment Variables (`.env`)
```bash
REDDIT_CLIENT_ID=your_id
REDDIT_CLIENT_SECRET=your_secret
REDDIT_USER_AGENT=TrendVision/1.0
SUBREDDITS=technology+ai+news
USE_TRANSFORMER=false  # Set true for DistilBERT accuracy
```

### 4. Launch the Platform
```bash
streamlit run UI.py
```
*Note: On first run, navigate to **Settings** and click **Initialize System** to build your local database.*

---

## 📂 Project Structure
```text
TrendVision/
├── UI.py                   # Main Dashboard & AI Logic
├── styles.css              # Glassmorphic Design System
├── app.py                  # Reddit Data Ingestion
├── nlp/                    # Keyword & Sentiment Engines
├── forecast/               # Prophet Forecasting Logic
├── pages/                  # Modular Feature Pages
│   ├── 1_Overview.py
│   ├── 2_Deep_Dive.py
│   ├── 5_News_Monitor.py
│   └── 6_Comparison.py
└── data/                   # Local Data Store (CSV)
```

---

## 💡 Troubleshooting

### Windows Long Path Error
If you encounter `[Errno 2]` during Prophet installation:
1. Open **PowerShell** as Administrator.
2. Run this command to enable long paths:
   ```powershell
   New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
   ```
3. Restart your terminal and try `pip install -r requirements.txt` again.

---

## 📜 License
This project is licensed under the MIT License. Built with ❤️ for the Open Source community.