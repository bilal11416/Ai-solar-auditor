import streamlit as st
import os
from groq import Groq

# Streamlit Page Setup
st.set_page_config(page_title="AI Solar Auditor", page_icon="⚡", layout="wide")

st.title("⚡ AI Solar Auditor (Public Version)")
st.write("Apne ghar ya shop ke bill ka data enter karein aur instant Solar Sizing & ROI Report haasil karein.")

# --- SECURE API KEY FETCH ---
# This looks for the hidden key in Streamlit Cloud Dashboard settings
if "GROQ_API_KEY" in st.secrets:
    HIDDEN_GROQ_KEY = st.secrets["GROQ_API_KEY"]
elif os.environ.get("GROQ_API_KEY"):
    HIDDEN_GROQ_KEY = os.environ.get("GROQ_API_KEY")
else:
    HIDDEN_GROQ_KEY = None

# Sidebar UI Configuration
with st.sidebar:
    st.header("⚙️ System Status")
    if HIDDEN_GROQ_KEY:
        st.success("✅ AI Engine Connected Securely")
    else:
        st.error("❌ AI Engine Disconnected")
    st.markdown("---")
    st.info("Designed by Bilal (Electrical Engineering). Public Open Access Version.")

# Form Input for Public Users
st.subheader("📋 Enter Electricity Bill Parameters")
col_input1, col_input2 = st.columns(2)

with col_input1:
    s_load = st.number_input("Sanctioned Load (kW):", min_value=1.0, value=5.0, step=1.0)
    tariff = st.text_input("Tariff Category:", value="A-1(76)")

with col_input2:
    units = st.number_input("Current Month Units (kWh):", min_value=1, value=700)
    bill_amount = st.number_input("Approximate Bill Amount (PKR):", min_value=0, value=35000)

if st.button("🚀 Run AI Solar Audit"):
    if not HIDDEN_GROQ_KEY:
        st.error("System configuration error: API Key is missing in Streamlit Secrets.")
    else:
        with st.spinner("🤖 AI Solar Expert is analyzing your parameters..."):
            try:
                client = Groq(api_key=HIDDEN_GROQ_KEY)
                simulated_bill_data = f"""
                - Sanctioned Load (kW): {s_load} kW
                - Tariff Category: {tariff}
                - Current Month Units (kWh): {units} kWh
                - Total Bill Amount (PKR): {bill_amount} PKR
                """
                
                engineer_prompt = f"""
                You are an expert Solar Engineer and Financial Analyst specializing in Pakistan's Net-Metering system.
                Based on the following electricity bill data, perform your engineering calculations:
                
                {simulated_bill_data}
                
                Provide a professional, highly-structured markdown report with:
                1. **⚡ Recommended Solar System Capacity (kW)**: Calculate optimal kW size based on the units. Ensure it is strictly within the Sanctioned Load limit.
                2. **🛠️ Technical Specifications**: Number of Solar Panels required (assuming 550W panels) and recommended Inverter Type (On-Grid with Net-Metering).
                3. **💰 Financial Estimate & Savings**: Approximate system cost in PKR (current Pakistan market rates), monthly bill reduction, and exact Payback Period (ROI) in years.
                
                Keep the output technical, clear, and structured with clear markdown bullet points. Do not include any extra introductory chat.
                """
                
                response = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[{"role": "user", "content": engineer_prompt}],
                    temperature=0.2
                )
                
                st.success("✅ Audit Report Generated Successfully!")
                st.markdown("### 📊 Final Audit Report")
                
                if hasattr(response, 'choices') and len(response.choices) > 0:
                    choice = response.choices
                    if hasattr(choice, 'message') and hasattr(choice.message, 'content'):
                        st.markdown(choice.message.content)
                else:
                    st.write(str(response))
                    
            except Exception as e:
                st.error(f"Execution Error: {e}")
