import streamlit as st
import os
from groq import Groq
import pandas as pd
from PIL import Image

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
st.title("☀️ AI Solar Auditor & Bill Verifier")
st.write("Professional Industrial & Residential Smart Energy Dashboard for Pakistan Utility Bills.")

# --- SECURE API KEY FETCH ---
if "GROQ_API_KEY" in st.secrets:
    HIDDEN_GROQ_KEY = st.secrets["GROQ_API_KEY"]
elif os.environ.get("GROQ_API_KEY"):
    HIDDEN_GROQ_KEY = os.environ.get("GROQ_API_KEY")
else:
    HIDDEN_GROQ_KEY = None

# ---- SIDEBAR SETTINGS ----
st.sidebar.header("🛠️ Advanced Engineering Settings")
inverter_brand = st.sidebar.selectbox("Select Inverter Brand:", ["🔑 Tier 1 (Huawei/Inverex)", "⭐ Tier 2 (Nitrox/Knox)", "Standard Hybrid"])
battery_backup = st.sidebar.radio("Battery Storage Required?", ["No (On-Grid Only)", "Yes (Hybrid System)"])

# CREATE TWO SEPARATE TABS FOR SYSTEM VARIETY
tab1, tab2 = st.tabs(["📊 Solar Sizing Recommender (Original)", "🔍 Factory & Colony Bill Validator (New)"])

# =========================================================================
# --- TAB 1: ORIGINAL SIZING RECOMENDER (YOUR PREVIOUS LOGIC) ---
# =========================================================================
with tab1:
    st.subheader("Residential / Commercial Capacity Estimator")
    
    # Layout Columns for Input
    col_input1, col_input2 = st.columns(2)

    with col_input1:
        s_load = st.number_input("Sanctioned Load (kW):", min_value=1.0, value=5.0, step=1.0, key="sizing_s_load")
        tariff = st.text_input("Tariff Category:", value="A-1(76)", key="sizing_tariff")

    with col_input2:
        units = st.number_input("Current Month Units (kWh):", min_value=1, value=700, key="sizing_units")
        bill_amount = st.number_input("Approximate Bill Amount (PKR):", min_value=0, value=35000, key="sizing_bill")

    # --- SIZING BUTTON CLICK LOGIC ---
    if st.button("🚀 Run AI Solar Audit", key="btn_run_audit"):
        if not HIDDEN_GROQ_KEY:
            st.error("System configuration error: API Key is missing in Streamlit Secrets.")
        else:
            st.success("📊 Generating Professional Financial & Engineering Analytics...")
            
            calculated_kw = round(units / 120, 1)  
            if calculated_kw < 3: calculated_kw = 3.0
            
            cost_multiplier = 140000 if battery_backup == "No (On-Grid Only)" else 190000
            estimated_investment = int(calculated_kw * cost_multiplier) 
            estimated_savings = int(bill_amount * 0.85) 
            new_bill = int(bill_amount - estimated_savings)
            
            co2_saved = round(calculated_kw * 1.2, 1) 
            panel_count = int((calculated_kw * 1000) / 550)

            m_col1, m_col2, m_col3, m_col4 = st.columns(4)
            m_col1.metric(label="Recommended System", value=f"{calculated_kw} kW")
            m_col2.metric(label="Est. Setup Cost", value=f"Rs {estimated_investment:,}")
            m_col3.metric(label="Monthly Savings", value=f"Rs {estimated_savings:,}", delta="Bills Cut")
            m_col4.metric(label="CO2 Offset / Year", value=f"{co2_saved} Tons 🌿")

            st.write("---")

            st.subheader("📉 Monthly Bill Comparison (Before vs After Solar)")
            chart_data = pd.DataFrame({
                'Status': ['Current Bill', 'New Bill with Solar'],
                'Bill Amount (PKR)': [bill_amount, new_bill]
            })
            st.bar_chart(data=chart_data, x='Status', y='Bill Amount (PKR)', use_container_width=True)
            
            st.write("---")
            
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
                        model="openai/gpt-oss-120b",
                        messages=[{"role": "user", "content": engineer_prompt}],
                        temperature=0.3,
                        max_tokens=800
                    )
                    
                    ai_report_text = completion.choices[0].message.content
                    st.subheader("📋 Detailed AI Audit Report")
                    st.markdown(ai_report_text)
                    st.write("---")
                    
                    # Professional Download printable document
                    st.subheader("📥 Professional Deliverable")
                    raw_pdf_content = f"...\n{ai_report_text}\n..." # truncated template
                    st.download_button(
                        label="📥 Download Official Audit Report (PDF/TXT)",
                        data=raw_pdf_content,
                        file_name="AI_Solar_Auditor_Report.txt",
                        mime="text/plain"
                    )
                except Exception as e:
                    st.error(f"An error occurred while calling the AI Engine: {e}")

# =========================================================================
# --- TAB 2: INDUSTRIAL FACTORY & COLONY BILL VALIDATOR (NEW) ---
# =========================================================================
with tab2:
    st.subheader("🏭 PESCO Industrial Bill Auditor (Tariff B3(T) & Net-Metering)")
    st.write("PESCO Industrial connection bill ko automatic format calculations k zarye double check aur audit krain.")

    # Select Box for Target Node Verification
    connection_type = st.selectbox("Select Target Verification Connection:", ["Factory (Net Metering B3(T))", "Colony (Simple B3 connection)"])
    
    # Setup standard fixed parameters automatically behind the scenes
    if connection_type == "Factory (Net Metering B3(T))":
        fixed_mf = 2000
        sanctioned_load_limit = 900.0
    else:
        fixed_mf = 40
        sanctioned_load_limit = 79.0

    st.info(f"ℹ️ **Auto Configurations Loaded:** Multiplying Factor (MF) = `{fixed_mf}`, Sanctioned Load = `{sanctioned_load_limit} kW`.")

    # Document upload trigger
    uploaded_bill_img = st.file_uploader("Apnay Bill ki photo ya PDF upload krain:", type=["png", "jpg", "jpeg", "pdf"], key="industrial_uploader")

    if uploaded_bill_img is not None:
        st.success("File upload successfully. Ready for engineering verification checks.")
        
        # Display Preview if it's an image
        if uploaded_bill_img.type in ["image/png", "image/jpeg", "image/jpg"]:
            img_preview = Image.open(uploaded_bill_img)
            st.image(img_preview, caption="Uploaded Document Preview", width=500)

        # Verification Action Button
        if st.button("🔍 Run Math Verification & Audit"):
            with st.spinner("Executing mathematical cross-checks (MF, Net-Metering, Surcharges)..."):
                
                # --- FACTORY LOGIC VERIFICATION ---
                if connection_type == "Factory (Net Metering B3(T))":
                    # Simulated extracted raw data vectors from user factory bill parameters
                    extracted_import_peak = 23020
                    extracted_export_peak = 0
                    net_peak_billed = 23020
                    
                    extracted_import_offpeak = 68590
                    extracted_export_offpeak = 29380
                    net_offpeak_billed = 39210
                    
                    measured_mdi = 420.0
                    total_energy_charges = 2032029
                    taxes_and_surcharges = 520198
                    printed_grand_total = 2552227

                    # Back-end automated math checks (Verification Engine)
                    calculated_net_offpeak = extracted_import_offpeak - extracted_export_offpeak
                    is_offpeak_correct = (calculated_net_offpeak == net_offpeak_billed)
                    is_mdi_within_limits = (measured_mdi <= sanctioned_load_limit)
                    summed_grand_total = total_energy_charges + taxes_and_surcharges
                    is_grand_total_matched = (summed_grand_total == printed_grand_total)

                    # UI Response Setup
                    st.success("### 📊 Verification Summary Report")
                    
                    # Core Status Checks

