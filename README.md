# 📊 AI Data Analyst

> Upload any CSV dataset and instantly get **descriptive statistics**, **interactive charts**, and **AI-powered business insights** — all in your browser.

Built with **Streamlit · Groq LLaMA 3 · Pandas · Seaborn/Matplotlib**

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-red?style=flat-square&logo=streamlit)
![Groq](https://img.shields.io/badge/Groq-LLaMA%203.3%2070B-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📂 **CSV Upload** | Drag-and-drop any CSV file — date columns auto-detected |
| 🗃️ **Dataset Overview** | Row count, column count, missing values, column types |
| 📐 **Descriptive Stats** | mean, std, min/max, quartiles for all numeric columns |
| 🏷️ **Category Breakdown** | Value counts for all categorical columns |
| 📈 **Revenue Trend** | Monthly time-series line chart |
| 🏆 **Product Performance** | Horizontal bar chart ranked by revenue |
| 🗂️ **Category Comparison** | Side-by-side bar + donut chart |
| 🔗 **Correlation Heatmap** | Numeric feature correlation matrix |
| 📊 **Distribution Plot** | Histogram + KDE for key numeric columns |
| 🤖 **AI Insights** | LLaMA 3.3 70B business analysis with recommendations |
| ⬇️ **Export** | Download AI insights as a `.txt` file |

---

## 🏗️ Project Structure
```
AI-Data-Analyst/
│
├── app/                        # Main application package
│   ├── main.py                 # Streamlit UI — entry point
│   ├── config.py               # Centralised settings & constants
│   │
│   ├── agents/
│   │   └── analyst_agent.py    # Orchestration layer
│   │
│   ├── analysis/
│   │   ├── data_loader.py      # CSV I/O, schema detection
│   │   ├── statistics.py       # Descriptive stats & LLM summaries
│   │   └── visualization.py    # All chart functions
│   │
│   └── utils/
│       └── prompts.py          # LLM prompt templates
│
├── data/
│   └── sample_sales.csv        # Built-in demo dataset
│
├── requirements.txt
├── run.py
├── .env.example
├── .gitignore
└── README.md
```

---

## ⚡ Quick Start

### Prerequisites
- Python 3.10+
- Free Groq API key → [console.groq.com](https://console.groq.com)

### 1. Clone the repository
```bash
git clone https://github.com/sreenugopireddy/AI-Data-Analyst.git
cd AI-Data-Analyst
```

### 2. Create a virtual environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\Activate.ps1

# macOS / Linux
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure your API key
```bash
cp .env.example .env
```
Open `.env` and add your key:
```env
GROQ_API_KEY=gsk_your_api_key_here
```

### 5. Run the app
```bash
streamlit run app/main.py
```
Open **http://localhost:8501** in your browser 🚀

---

## 🔧 Configuration

All settings live in `app/config.py`:
```python
GROQ_MODEL       = "llama-3.3-70b-versatile"  # LLM model
GROQ_MAX_TOKENS  = 1024                         # Max response length
GROQ_TEMPERATURE = 0.4                          # 0 = factual, 1 = creative
```

**Available Groq Models:**

| Model | Speed | Quality |
|-------|-------|---------|
| `llama-3.3-70b-versatile` | Fast | ⭐⭐⭐⭐⭐ Best |
| `llama-3.1-8b-instant` | Fastest | ⭐⭐⭐ Good |
| `mixtral-8x7b-32768` | Fast | ⭐⭐⭐⭐ Great |
| `gemma2-9b-it` | Fast | ⭐⭐⭐ Good |

---

## 💰 Cost Estimate

| Usage | Monthly Cost |
|-------|-------------|
| Personal / demo (< 100 clicks/day) | **$0 — Free tier** |
| Small team (500 clicks/day) | **~$1–3/month** |
| Production (10,000 clicks/day) | **~$20–40/month** |

---

## 🚀 Deployment — Streamlit Cloud (Free)

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Add secret under **App Settings → Secrets**:
```toml
GROQ_API_KEY = "gsk_your_api_key_here"
```
5. Click **Deploy** ✅

---

## 🛠️ Tech Stack

| Technology | Purpose |
|-----------|---------|
| [Streamlit](https://streamlit.io) | Web UI framework |
| [Groq](https://groq.com) | Ultra-fast LLM inference |
| [LLaMA 3.3 70B](https://groq.com) | AI insights generation |
| [Pandas](https://pandas.pydata.org) | Data manipulation |
| [Matplotlib](https://matplotlib.org) | Chart rendering |
| [Seaborn](https://seaborn.pydata.org) | Statistical visualisation |
| [python-dotenv](https://github.com/theskumar/python-dotenv) | Environment variables |

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

## 👤 Author

**Sreenuva Gopireddy**
- GitHub: [@sreenugopireddy](https://github.com/sreenugopireddy)

---

<p align="center">Built with ❤️ using Streamlit and Groq</p>
