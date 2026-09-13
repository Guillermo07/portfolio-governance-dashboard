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

```text
[ Google Sheets ] ---> [ st.connection / GSheets ] ---> [ Pandas Processing Engine ] ---> [ Streamlit UI ]
 (Dynamic Source)          (60s TTL Cache)               (Burn Rate & Variance)         (Metrics & Charts)
```

---
## System Architecture
* Language: Python 3.10+
* Frontend / Framework: Streamlit
* Data Manipulation: Pandas
* Data Integration: st-gsheets-connection (Google Sheets API)
* Version Control & CI/CD: Git, GitHub, Streamlit Community Cloud

---
## Key Metrics Calculated
* Burn Rate: (Actual Spend / Allocated Budget) * 100
* Financial Variance: Allocated Budget - Actual Spend
* Budget Health Distribution: Aggregate spend categorized by operational tribe.

---
## Local Setup & Installation

1. Clone the repository: 
git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
cd YOUR_REPO_NAME
cd portfolio
2. Set up a virtual enviroment:
python -m venv .ven.\.ven\Scripts\Activate.ps1
3. Install depedencies:
pip install -r requirements.txt
4. Launch the application:
streamlit run app.py