<div align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/UI-Glassmorphism-purple?style=for-the-badge" />

  # 🚀 TrendVision AI
  **The Ultimate Social Intelligence & Predictive Analytics Suite**

  *Bridging the gap between raw social chatter and actionable market intelligence.*
</div>

---

## 📖 Table of Contents
- Overview
- Key Features
- Architecture
- Tech Stack
- Getting Started
- Roadmap
- License

---

## 🌐 Overview
TrendVision AI is a high-fidelity analytical platform designed to monitor, analyze, and forecast social media trends in real-time. By leveraging **Transformer-based NLP** and **Glassmorphic UI/UX**, it transforms unstructured data from Reddit and global news into a structured, predictive dashboard.

> **Why TrendVision?** In a digital-first world, signals often get lost in the noise. TrendVision uses AI to amplify those signals, providing a 7-day forecast of community engagement and sentiment shifts.

---

## ✨ Key Features

### 🤖 AI-Powered UI & UX
*   **Glassmorphic Design**: A futuristic interface utilizing backdrop-blur effects and semi-transparent panels.
*   **Smart Contextual Briefings**: The dashboard dynamically generates "AI Briefings" based on real-time sentiment spikes.
*   **Micro-Interactions**: Purpose-driven animations (Lottie & CSS) that provide tactile feedback.

###  Advanced Analytics Pipeline
*   **Semantic Keyword Extraction**: Uses **KeyBERT** to identify contextually relevant phrases rather than just high-frequency words.
*   **Hybrid Sentiment Engine**: Toggles between **TextBlob** (speed) and **DistilBERT** (accuracy) to provide deep emotional insights.
*   **Predictive Forecasting**: Implements **Facebook Prophet** to model engagement volume for the upcoming week.

### 📡 Multi-Channel Intelligence
*   **Reddit Intelligence**: Deep-scans subreddits for emerging discussions.
*   **Global News Monitor**: Correlates social trends with real-world events via RSS integration.
*   **Community Benchmarking**: Side-by-side comparison of subreddit performance and sentiment.

---

## 🏗️ Architecture
TrendVision follows a modular pipeline architecture:
1.  **Ingestion**: Asynchronous data fetching via PRAW (Reddit) and Feedparser (News).
2.  **Processing**: NLP layer handles cleaning, keyword extraction (KeyBERT), and sentiment scoring.
3.  **Analytics**: Time-series modeling via Prophet for volume forecasting.
4.  **Visualization**: Streamlit-based frontend with Plotly and custom CSS.

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

## ⚙️ Getting Started

### 1. Prerequisites
*   Python 3.9 or higher
*   Reddit API Credentials (Create them here)

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/trendvision.git
cd trendvision

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration (`.env`)
Create a `.env` file in the root directory:
```env
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=TrendVision/1.0
SUBREDDITS=technology+ai+news+crypto
USE_TRANSFORMER=false  # Set to true for high-accuracy DistilBERT
```

### 4. Run the Platform
```bash
streamlit run UI.py
```
*Note: On your first visit, go to the **Settings** page and click **"Initialize System"** to populate your local database.*

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
│   ├── 1_Overview.py       # KPI & Sentiment Distribution
│   ├── 2_Deep_Dive.py      # Keyword Analysis & Comparison
│   ├── 5_News_Monitor.py   # RSS News Integration
│   └── 6_Comparison.py     # Subreddit Benchmarking
└── data/                   # Local Data Store (CSV)
```

---

## 🚀 Roadmap
- [ ] **Multi-Platform Support**: Integrate Twitter (X) and YouTube comment analysis.
- [ ] **Real-Time Alerts**: Webhook support for Discord and Microsoft Teams.
- [ ] **Advanced Topic Modeling**: Full BERTopic visualization suite.
- [ ] **Export Engine**: Generate PDF/Excel reports for stakeholders.

---

## � Troubleshooting

### Windows Long Path Error
If you encounter `[Errno 2]` during Prophet installation:
1. Open **PowerShell** as Administrator.
2. Run:
   ```powershell
   New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
   ```
3. Restart your terminal and reinstall.

---

## 🤝 Contributing
Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📜 License
Distributed under the MIT License. See `LICENSE` for more information.

<div align="center">
  Built with ❤️ by Niti patel
</div>