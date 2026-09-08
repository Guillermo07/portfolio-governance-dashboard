import pandas as pd
import streamlit as st

# Page setup
st.set_page_config(page_title="Portfolio Governance", layout="wide")
st.title("📊 Portfolio Governance Dashboard")

# 1. Dataset
data = {
    "Project_Name": [
        "Cloud Migration",
        "Payment Gateway V2",
        "AI Fraud Engine",
        "Core Banking Modernization",
    ],
    "Project_Type": [
        "Infrastructure",
        "Product",
        "Automation / AI",
        "Core Tech",
    ],
    "Allocated_Budget": [150000, 85000, 120000, 300000],
    "Actual_Spend": [45000, 80000, 60000, 210000],
    "Start_Date": ["2026-01-15", "2026-03-01", "2026-04-10", "2026-02-01"],
    "Estimated_End_Date": [
        "2026-11-30",
        "2026-06-15",
        "2026-10-01",
        "2026-12-31",
    ],
    "Progress_Pct": [35, 90, 50, 70],
    "Risk_Status": ["Low", "High", "Medium", "Medium"],
}
df = pd.DataFrame(data)

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