import streamlit as st
import random

# App Title
st.title("💳 Credit Card Fraud Detection (Prototype)")

# Description
st.markdown("This is a prototype interface for detecting fraudulent online banking transactions.")

# --- Inputs ---
st.subheader("Enter Transaction Details:")

amount = st.number_input("Transaction Amount (RM)", min_value=0.0, format="%.2f")

category = st.selectbox("Transaction Category", [
    "shopping_net", "shopping_pos", "grocery_pos", "travel",
    "entertainment", "personal_care", "misc_net"
])

latitude = st.number_input("User Latitude", format="%.6f")
longitude = st.number_input("User Longitude", format="%.6f")

hour = st.slider("Transaction Hour", 0, 23, 12)

# --- Predict Button ---
if st.button("Predict Fraud"):
    # Dummy logic: just randomly decide fraud vs not fraud
    is_fraud = random.choice([0, 1])
    probability = random.uniform(70, 99.9)

    st.subheader("🔍 Prediction Result:")

    if is_fraud:
        st.error(f"🚨 Fraud Detected! (Probability: {probability:.2f}%)")
    else:
        st.success(f"✅ Legitimate Transaction (Probability: {100 - probability:.2f}%)")

# Footer
st.markdown("---")
st.caption("This is a dummy prototype. No real model is used yet.")
