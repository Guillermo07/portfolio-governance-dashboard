import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from google import genai


# 1. Page Configuration
st.set_page_config(page_title="Executive Governance Dashboard", layout="wide")

# 2. Establish Google Sheets Connection & Fetch Data
SHEET_URL = "https://docs.google.com/spreadsheets/d/1-oK2aczwg_bOiAPXY02IG3mATUspXYumwkVyN_G3Xvo/edit?gid=1501653939#gid=1501653939"

conn = st.connection("gsheets", type=GSheetsConnection)
# ttl=60 caches data for 60 seconds so it doesn't re-fetch on every single click
df = conn.read(spreadsheet=SHEET_URL, ttl=60)

# Drop any blank rows that might exist at the bottom of the sheet
df = df.dropna(subset=["Project_Name"])

# Calculate Burn_Rate and Variance if they don't already exist
df["Burn_Rate"] = (df["Actual_Spend"] / df["Allocated_Budget"]) * 100
df["Variance"] = df["Allocated_Budget"] - df["Actual_Spend"]

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

# ---------------------------------------------------------
# 6. AI Executive Variance & Risk Analyst
# ---------------------------------------------------------
 
st.divider()
st.subheader("🤖 AI Executive Variance & Risk Analyst")

if st.button("Generate Executive Brief", type="primary"):
    with st.spinner("Analyzing portfolio risk, variances, and delivery health..."):
        # 1. Initialize client using your secret
        client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

        # 2. Format portfolio data cleanly
        data_summary = df[["Project_Name", "Tribe", "Status", "Allocated_Budget", "Actual_Spend"]].to_string(index=False)

        prompt = f"""
        You are a seasoned Technology Portfolio Director and Strategy Lead.
        Analyze the following active portfolio data and deliver a concise, high-impact Executive Brief:

        {data_summary}

        Structure your response clearly with these three standalone sections:
        1. **Portfolio Health Overview**: A 2-sentence macro summary of portfolio delivery and financial posture.
        2. **Critical Flags & Cost Variances**: Explicitly call out projects with high budget burn or 'Blocked' status, stating the financial impact.
        3. **Strategic Recommendations**: 2-3 immediate, actionable operational steps (e.g., budget reallocation, executive escalation, de-scoping).

        Keep the tone candid, pragmatic, and executive-ready. Avoid fluff.
        """

        # 3. Call the modern 2.5 Flash model
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
        )

        # 4. Render output
        st.markdown(response.text)

# ---------------------------------------------------------
# 7. Conversational AI Assistant (Module 2.2)
# ---------------------------------------------------------

st.divider()
st.subheader("💬 Query the Portfolio")
st.caption("Ask questions about tribe allocation, specific project risks, or request draft communications.")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display prior chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input widget
if user_prompt := st.chat_input("E.g., Which projects are at risk of running out of budget?"):
    # 1. Display and record the user prompt
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # 2. Build ground-truth context from current dataframe
    portfolio_context = df[["Project_Name", "Tribe", "Status", "Allocated_Budget", "Actual_Spend", "Burn_Rate", "Variance"]].to_string(index=False)

    system_instruction = f"""
You are an expert Strategic Portfolio Management Assistant.
You have direct access to the live portfolio data below:

{portfolio_context}

Instructions:
- Answer user questions accurately using ONLY the provided data.
- If calculating figures, be precise with numbers and percentages.
- If asked to draft emails, Slack updates, or meeting agendas, maintain an executive, candid, and professional tone.
- If the user asks something outside the scope of this portfolio, politely state that you only have access to current portfolio governance data.
"""

    # 3. Assemble the conversation history payload
    conversation = [
        {"role": "user", "parts": [{"text": system_instruction}]}
    ]
    for m in st.session_state.messages:
        api_role = "user" if m["role"] == "user" else "model"
        conversation.append({"role": api_role, "parts": [{"text": m["content"]}]})

    # 4. Request answer with fallback model candidates
    with st.chat_message("assistant"):
        with st.spinner("Analyzing portfolio..."):
            client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

            target_models = [
                "gemini-3.6-flash",
                "gemini-2.0-flash",
                "gemini-1.5-flash",
            ]
            reply_text = None

            for model_candidate in target_models:
                try:
                    response = client.models.generate_content(
                        model=model_candidate,
                        contents=conversation,
                    )
                    reply_text = response.text
                    break
                except Exception as e:
                    print(f"Failed with {model_candidate}: {e}")
                    continue

            if reply_text:
                st.markdown(reply_text)
                st.session_state.messages.append({"role": "assistant", "content": reply_text})
            else:
                st.error("The portfolio intelligence engine is currently overloaded. Please retry in a few moments.")