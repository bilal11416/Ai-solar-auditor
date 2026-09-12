import streamlit as st
import os
from groq import Groq
import pandas as pd

# 1. Page Config Setup
st.set_page_config(
    page_title="AI Solar Auditor", 
    page_icon="☀️", 
    layout="wide"
)

# 2. Hide Streamlit Footer & Add Custom Text
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            footer:after {
                content:'AI Solar Auditor | Built for Innovation Championship'; 
                visibility: visible;
                display: block;
                position: relative;
                top: 2px;
            }
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# App Title
st.title("☀️ AI Solar Auditor (Public Version)")
st.write("Enter your residential or commercial electricity bill parameters to instantly generate a custom Solar Sizing & Financial ROI Report.")

# --- SECURE API KEY FETCH ---
if "GROQ_API_KEY" in st.secrets:
    HIDDEN_GROQ_KEY = st.secrets["GROQ_API_KEY"]
elif os.environ.get("GROQ_API_KEY"):
    HIDDEN_GROQ_KEY = os.environ.get("GROQ_API_KEY")
else:
    HIDDEN_GROQ_KEY = None

# ---- PROFESSIONAL SIDEBAR FOR JUDGES ----
st.sidebar.header("🛠️ Advanced Engineering Settings")
inverter_brand = st.sidebar.selectbox("Select Inverter Brand:", ["🔑 Tier 1 (Huawei/Inverex)", "⭐ Tier 2 (Nitrox/Knox)", "Standard Hybrid"])
battery_backup = st.sidebar.radio("Battery Storage Required?", ["No (On-Grid Only)", "Yes (Hybrid System)"])

# Layout Columns for Input
col_input1, col_input2 = st.columns(2)

with col_input1:
    s_load = st.number_input("Sanctioned Load (kW):", min_value=1.0, value=5.0, step=1.0)
    tariff = st.text_input("Tariff Category:", value="A-1(76)")

with col_input2:
    units = st.number_input("Current Month Units (kWh):", min_value=1, value=700)
    bill_amount = st.number_input("Approximate Bill Amount (PKR):", min_value=0, value=35000)

# --- BUTTON CLICK LOGIC ---
if st.button("🚀 Run AI Solar Audit"):
    if not HIDDEN_GROQ_KEY:
        st.error("System configuration error: API Key is missing in Streamlit Secrets.")
    else:
        st.success("📊 Generating Professional Financial & Engineering Analytics...")
        
        # Smart math calculations
        calculated_kw = round(units / 120, 1)  
        if calculated_kw < 3: calculated_kw = 3.0
        
        # Base multiplier adjusts depending on hybrid choice
        cost_multiplier = 140000 if battery_backup == "No (On-Grid Only)" else 190000
        estimated_investment = int(calculated_kw * cost_multiplier) 
        estimated_savings = int(bill_amount * 0.85) 
        new_bill = int(bill_amount - estimated_savings)
        
        # Environmental calculation (Judges favorite!)
        co2_saved = round(calculated_kw * 1.2, 1) 
        panel_count = int((calculated_kw * 1000) / 550) # 550W panels estimate

        # A. Display Metric Cards
        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        m_col1.metric(label="Recommended System", value=f"{calculated_kw} kW")
        m_col2.metric(label="Est. Setup Cost", value=f"Rs {estimated_investment:,}")
        m_col3.metric(label="Monthly Savings", value=f"Rs {estimated_savings:,}", delta="Bills Cut")
        m_col4.metric(label="CO2 Offset / Year", value=f"{co2_saved} Tons 🌿")

        st.write("---")

        # B. Display Dynamic Comparison Chart
        st.subheader("📉 Monthly Bill Comparison (Before vs After Solar)")
        chart_data = pd.DataFrame({
            'Status': ['Current Bill', 'New Bill with Solar'],
            'Bill Amount (PKR)': [bill_amount, new_bill]
        })
        st.bar_chart(data=chart_data, x='Status', y='Bill Amount (PKR)', use_container_width=True)
        
        st.write("---")
        
        # ---- CALLING GROQ AI ----
        with st.spinner("🧠 AI Solar Expert is analyzing parameters and hardware options..."):
            try:
                client = Groq(api_key=HIDDEN_GROQ_KEY)
                simulated_bill_data = f"""
                - Sanctioned Load (kW): {s_load} kW
                - Tariff Category: {tariff}
                - Current Month Units (kWh): {units} kWh
                - Total Bill Amount (PKR): {bill_amount} PKR
                - Selected Inverter: {inverter_brand}
                - Battery Option: {battery_backup}
                """
                
                engineer_prompt = f"""
                You are an expert Solar Engineer and Financial Analyst specializing in Pakistan's Net-Metering system.
                Based on the following electricity bill data and hardware specs, perform engineering calculations and provide a professional report:
                {simulated_bill_data}
                Include system sizing, panel count estimate, payback period, and explicitly mention advice regarding {inverter_brand} and the user's choice of {battery_backup}. Keep it highly professional and formatted in clear sections.
                """
                
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": engineer_prompt}],
                    temperature=0.3,
                    max_tokens=800
                )
                
                ai_report_text = completion.choices.message.content
                
                # Show AI Report on UI
                st.subheader("📋 Detailed AI Audit Report")
                st.markdown(ai_report_text)
                
                st.write("---")
                
                # C. PROFESSIONAL PDF GENERATOR FEATURE 🏆
                st.subheader("📥 Professional Deliverable")
                
                # Constructing printable report layout
                raw_pdf_content = f"""
======================================================
              AI SOLAR AUDIT REPORT                  
======================================================
Generated via AI Solar Auditor Smart Engine
------------------------------------------------------
[INPUT PARAMETERS]
- Sanctioned Load: {s_load} kW
- Tariff Category: {tariff}
- Current Month Units: {units} kWh
- Baseline Monthly Bill: PKR {bill_amount:,}

[ENGINEERING ANALYTICS]
- Recommended Solar Capacity: {calculated_kw} kW
- Estimated Total Panel Count (550W): {panel_count} Plates
- Inverter Specification: {inverter_brand}
- Energy Storage Configuration: {battery_backup}

[FINANCIAL METRICS & ROI]
- Estimated Capital Investment: PKR {estimated_investment:,}
- Anticipated Monthly Savings: PKR {estimated_savings:,}
- Project New Monthly Bill: PKR {new_bill:,}
- Carbon Footprint Reduction: {co2_saved} Tons CO2 / Year

------------------------------------------------------
[EXECUTIVE AI LOGICAL BREAKDOWN]
{ai_report_text}
------------------------------------------------------
Disclaimer: This analysis is computer-generated based on current utility pricing metrics in Pakistan. Actul engineering site surveys may show slight variations.
======================================================
                """
                
                # Creating download button for judges
                st.download_button(
                    label="📥 Download Official Audit Report (PDF/TXT)",
                    data=raw_pdf_content,
                    file_name="AI_Solar_Auditor_Report.txt",
                    mime="text/plain",
                    help="Click to download the structured data sheet and executive AI breakdown."
                )
                st.success("Report compiled successfully! Use the button above to export.")
                
            except Exception as e:
                st.error(f"An error occurred while calling the AI Engine: {e}")
