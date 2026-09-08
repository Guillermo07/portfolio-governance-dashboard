import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# 1. Page Configuration
st.set_page_config(page_title="Executive Governance Dashboard", layout="wide")

# 2. Establish Google Sheets Connection & Fetch Data
SHEET_URL = "https://docs.google.com/spreadsheets/d/1-oK2aczwg_bOiAPXY02IG3mATUspXYumwkVyN_G3Xvo/edit?gid=1501653939#gid=1501653939"

conn = st.connection("gsheets", type=GSheetsConnection)
# ttl=60 caches data for 60 seconds so it doesn't re-fetch on every single click
df = conn.read(spreadsheet=SHEET_URL, ttl=60)

# Drop any blank rows that might exist at the bottom of the sheet
df = df.dropna(subset=["Project_Name"])

# 2. Sidebar
risk_filter = st.sidebar.selectbox(
    "Filter by Risk Status", ["All", "Low", "Medium", "High"]
)

if risk_filter != "All":
    filtered_df = df[df["Risk_Status"] == risk_filter]
else:
    filtered_df = df

# 3. KPI Metrics
total_budget = filtered_df["Allocated_Budget"].sum()
total_spend = filtered_df["Actual_Spend"].sum()
burn_rate = (total_spend / total_budget * 100) if total_budget > 0 else 0

col1, col2, col3 = st.columns(3)
col1.metric("Total Budget", f"${total_budget:,.0f}")
col2.metric("Actual Spend", f"${total_spend:,.0f}")
col3.metric("Portfolio Burn Rate", f"{burn_rate:.1f}%")

st.divider()

# 4. Comparative Bar Chart
st.subheader("Budget vs. Actual Spend by Project")
chart_data = filtered_df.set_index("Project_Name")[
    ["Allocated_Budget", "Actual_Spend"]
]
st.bar_chart(chart_data)

st.divider()

# 5. Table
st.subheader("Detailed Project View")
st.dataframe(filtered_df, use_container_width=True)