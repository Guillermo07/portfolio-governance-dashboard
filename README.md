# Executive Governance Dashboard

An interactive portfolio governance and financial tracking dashboard built with Python and Streamlit. Designed for portfolio managers and PMO leads to monitor tribe allocation, detect budget overruns, and track project health in real time.

🔗 **Live Demo:** [View Live Dashboard](https://portfolio-governance-dashboard-3zxsw87ia5z73fys7hxx8s.streamlit.app/)

---

## Business Problem & Context
Managing technology portfolio budgets across multiple functional tribes often relies on static spreadsheets, resulting in stale data, delayed risk identification, and cumbersome executive reporting. 

This dashboard provides executive visibility into:
* Real-time budget allocation versus actual spend across business tribes.
* Automated financial variance and burn-rate tracking.
* High-level health and delivery status monitoring (`On Track`, `Delayed`, `Blocked`).

---
## System Architecture

´´´ 
[ Google Sheets ] 
       │ (Dynamic Source / 60s TTL Cache)
       ▼
[ Streamlit Pipeline ] ───► [ Pandas Engine ] ───► [ Executive UI ]
                                   │                   │          │
                                   ▼                   ▼          ▼
                        [ Context Assembly ]   [ Brief Button ] [ Chat Input ]
                                   │                   │          │
                                   └─────────┬─────────┴──────────┘
                                             ▼
                                  [ Resilient Model Router ]
                                  (3.6-Flash ➔ 2.0-Flash ➔ 1.5-Flash)
´´´
---
## 🚀 Key Features

* Live Data Integration: Direct bi-directional connection to Google Sheets via st-gsheets-connection with time-to-live (TTL) caching to balance performance and freshness.
* Financial Health & Variance Tracking: Automated computation of project burn rates, financial variance, and cross-tribe budget allocation.
* AI Executive Risk Analyst: An embedded Gemini 3.6 Flash agent that ingests current portfolio data and outputs structured briefs containing:
    - Portfolio health overview
    - Critical flags and capital at risk (Burn Rate > 100% or Blocked)
    - Immediate strategic mitigation steps (resource rebalancing, stop-work recommendations)
* Zero-Trust Secret Management: API credentials and service account configs are isolated via .streamlit/secrets.toml locally and managed securely via Streamlit Cloud environment variables.
* **Interactive Conversational Copilot:** Built-in chat interface (`st.chat_input`, `st.chat_message`, `st.session_state`) allowing stakeholders to query allocation, project health, and capital-at-risk using natural language.
* **Resilient Multi-Model Failover:** Fault-tolerant LLM pipeline designed to handle API capacity spikes by gracefully falling back across model candidates (`gemini-3.6-flash`, `gemini-2.0-flash`, `gemini-1.5-flash`).

---
## 🛠️ Tech Stack
* Language: Python 3.10+
* Frontend / Framework: Streamlit
* AI & LLM: Google GenAI SDK (google-genai), Gemini 3.6 Flash
* Data Manipulation: Pandas
* Data Integration: st-gsheets-connection (Google Sheets API)
* Version Control & CI/CD: Git, GitHub, Streamlit Community Cloud

---
## 📊 Key Metrics Calculated
* Burn Rate: (Actual Spend / Allocated Budget) * 100
* Financial Variance: Allocated Budget - Actual Spend
* Budget Health Distribution: Aggregate spend categorized by operational tribe.

---
## 💻 Local Setup & Installation

1. Clone the repository: 
git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
cd YOUR_REPO_NAME
cd portfolio
2. Set up a virtual enviroment:
python -m venv .ven.\.ven\Scripts\Activate.ps1
3. Install depedencies:
pip install -r requirements.txt
4. Configure secrets:
Create .streamlit/secrets.toml and add your credentials:
GEMINI_API_KEY = "your_gemini_api_key"
5. Launch the application:
streamlit run app.py

