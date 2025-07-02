import streamlit as st
import google.generativeai as genai
from ml_models import predict_suspicion

# Configure Gemini
genai.configure(api_key=st.secrets["API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")

st.title("🕵️ Suspicious Login Pattern Analyzer")

st.markdown("Analyze login events to detect suspicious behavior using ML & Gemini AI.")

# Inputs
user_id = st.text_input("User ID", "user5")
location = st.text_input("Location", "Russia")
time_str = st.text_input("Time (HH:MM)", "02:30")
device = st.selectbox("Device", ["Laptop", "Phone", "Tablet", "Unknown"])

if st.button("Analyze Login"):
    with st.spinner("Analyzing..."):
        is_suspicious = predict_suspicion(location, time_str, device)
        
        # Gemini prompt
        prompt = f"""
        Login details:
        - User ID: {user_id}
        - Location: {location}
        - Time: {time_str}
        - Device: {device}
        ML prediction: {"Suspicious" if is_suspicious else "Normal"}.

        Provide:
        - Risk assessment summary
        - Suggested actions (e.g., block, MFA check, alert)
        - Short reasoning why it may be suspicious

        Present as friendly security advice for an admin.
        """

        response = model.generate_content(prompt)
        advice = response.text

        st.success("✅ Analysis Complete")
        st.markdown(f"**Prediction:** {'🚨 Suspicious' if is_suspicious else '✅ Normal'}")
        st.markdown("---")
        st.markdown(advice)

st.caption("🔒 Powered by ML, Gemini API & Streamlit")
