import streamlit as st
import pandas as pd
import random

# App Title
st.title("💳 Credit Card Fraud Detection (Prototype)")

st.markdown("This is a prototype interface for detecting fraudulent online banking transactions.")
st.markdown("Choose to test a **single transaction** or **upload a file** for batch prediction.")

# Mode Selection
mode = st.radio("Select Prediction Mode", ["🔘 Single Transaction", "📁 Upload File"])

# --- SINGLE TRANSACTION MODE ---
if mode == "🔘 Single Transaction":
    st.subheader("Enter Transaction Details:")

    amount = st.number_input("Transaction Amount (RM)", min_value=0.0, format="%.2f")

    category = st.selectbox("Transaction Category", [
        "shopping_net", "shopping_pos", "grocery_pos", "travel",
        "entertainment", "personal_care", "misc_net"
    ])

    latitude = st.number_input("User Latitude", format="%.6f")
    longitude = st.number_input("User Longitude", format="%.6f")

    hour = st.slider("Transaction Hour", 0, 23, 12)

    # Predict Button
    if st.button("Predict Fraud"):
        is_fraud = random.choice([0, 1])
        probability = random.uniform(70, 99.9)

        st.subheader("🔍 Prediction Result:")
        if is_fraud:
            st.error(f"🚨 Fraud Detected! (Probability: {probability:.2f}%)")
        else:
            st.success(f"✅ Legitimate Transaction (Probability: {100 - probability:.2f}%)")

# --- FILE UPLOAD MODE ---
else:
    st.subheader("📤 Upload Transaction File (CSV or Excel)")

    uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx"])

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            st.write("✅ File successfully uploaded. Preview below:")
            st.dataframe(df.head())

            if st.button("Run Dummy Fraud Detection"):
                # Add dummy fraud prediction column
                df['Fraud_Predicted'] = [random.choice(["Fraud", "Legit"]) for _ in range(len(df))]
                df['Probability (%)'] = [round(random.uniform(70, 99.9), 2) for _ in range(len(df))]

                st.success("Prediction completed!")
                st.dataframe(df)

                # Optional: download button
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Download Results", data=csv, file_name="fraud_predictions.csv", mime="text/csv")

        except Exception as e:
            st.error(f"❌ Error reading the file: {e}")

# Footer
st.markdown("---")
st.caption("This is a dummy prototype. No real model is used yet.")
