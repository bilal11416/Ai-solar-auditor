import streamlit as st
import os
from groq import Groq

# Streamlit Page Setup
st.set_page_config(page_title="AI Solar Auditor", page_icon="⚡", layout="wide")

st.title("⚡ AI Solar Auditor (Multi-Agent Simulation)")
st.write("Enter your PESCO/DESCO Bill data to instantly get an AI-powered Solar Sizing & Financial ROI Report.")

# Sidebar for API Key
with st.sidebar:
    st.header("⚙️ Configuration")
    groq_api_key = st.text_input("Enter Groq API Key:", type="password")
    st.markdown("---")
    st.info("Designed for Hackathon. Powered by Electrical Engineering logic.")

# Execution Logic
if not groq_api_key:
    st.warning("⚠️ Please enter your Groq API Key in the sidebar to run the auditor.")
else:
    # Initialize Groq Client safely
    client = Groq(api_key=groq_api_key)
    
    # Form Input for User
    st.subheader("📋 Enter Bill Parameters manually (Bypassing Image Rate Limits)")
    col_input1, col_input2 = st.columns(2)
    
    with col_input1:
        s_load = st.number_input("Sanctioned Load (kW):", min_value=1.0, value=79.0, step=1.0)
        tariff = st.text_input("Tariff Category:", value="A-1(76)")
    
    with col_input2:
        units = st.number_input("Current Month Units (kWh):", min_value=1, value=10267)
        bill_amount = st.number_input("Approximate Bill Amount (PKR):", min_value=0, value=650000)

    if st.button("🚀 Run AI Solar Audit"):
        with st.spinner("🤖 Agent 2 is calculating engineering requirements..."):
            try:
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
                
                # Request generation
                response = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[{"role": "user", "content": engineer_prompt}],
                    temperature=0.2
                )
                
                st.success("✅ Audit Report Generated Successfully!")
                st.markdown("### 📊 Final Audit Report")
                
                # --- UNIVERSAL PARSING FIX ---
                # This guarantees content prints regardless of response type structure
                if hasattr(response, 'choices') and len(response.choices) > 0:
                    choice = response.choices[0]
                    if hasattr(choice, 'message') and hasattr(choice.message, 'content'):
                        st.markdown(choice.message.content)
                    elif isinstance(choice, dict) and 'message' in choice:
                        st.markdown(choice['message'].get('content', ''))
                elif hasattr(response, 'content'):
                    st.markdown(response.content)
                else:
                    st.write(str(response))
                    
            except Exception as e:
                st.error(f"Execution Error: {e}")
