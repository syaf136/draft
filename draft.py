import streamlit as st
import pandas as pd
import random
from geopy.distance import geodesic

# -------------------------
# PAGE CONFIGURATION
# -------------------------
st.set_page_config(page_title="Fraud Detection System", page_icon="💳", layout="centered")

# -------------------------
# SIDEBAR
# -------------------------
with st.sidebar:
    st.title("⚙️ Options")
    mode = st.radio("Select Mode", ["🔘 Single Transaction", "📁 Upload CSV"])
    st.markdown("---")
    st.write("👤 Created by: Your Name")
    st.write("📅 FYP 2025")
    st.write("🔍 Status: Prototype")

# -------------------------
# HEADER
# -------------------------
st.markdown("<h1 style='text-align: center;'>💳 Credit Card Fraud Detection System</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>This prototype simulates fraud prediction for online banking transactions.</p>", unsafe_allow_html=True)
st.markdown("---")

# -------------------------
# HAVERSINE FUNCTION
# -------------------------
def haversine(lat1, lon1, lat2, lon2):
    return geodesic((lat1, lon1), (lat2, lon2)).km

# -------------------------
# SINGLE TRANSACTION MODE
# -------------------------
if mode == "🔘 Single Transaction":
    st.subheader("📥 Enter Transaction Details")

    col1, col2 = st.columns(2)
    with col1:
        merchant = st.text_input("Merchant Name")
        category = st.text_input("Transaction Category")
        amt = st.number_input("Transaction Amount (RM)", min_value=0.0, format="%.2f")
        hour = st.slider("Transaction Hour", 0, 23, 12)
    with col2:
        gender = st.selectbox("Gender", ["Male", "Female"])
        cc_num = st.text_input("Credit Card Number")
        day = st.slider("Transaction Day", 1, 31, 15)
        month = st.slider("Transaction Month", 1, 12, 6)

    st.markdown("📍 **Location Information**")
    col3, col4 = st.columns(2)
    with col3:
        lat = st.number_input("User Latitude", format="%.6f")
        long = st.number_input("User Longitude", format="%.6f")
    with col4:
        merch_lat = st.number_input("Merchant Latitude", format="%.6f")
        merch_long = st.number_input("Merchant Longitude", format="%.6f")

    distance = haversine(lat, long, merch_lat, merch_long)

    if st.button("🚨 Check for Fraud"):
        if merchant and category and cc_num:
            prediction = random.choice([0, 1])
            confidence = round(random.uniform(70, 99.9), 2)
            result = "🚨 Fraudulent Transaction" if prediction == 1 else "✅ Legitimate Transaction"

            st.markdown("---")
            st.subheader("🔍 Prediction Result")
            if prediction == 1:
                st.error(f"**{result}**  \nConfidence Score: `{confidence}%`")
            else:
                st.success(f"**{result}**  \nConfidence Score: `{confidence}%`")

            st.markdown(f"📏 Distance from User to Merchant: `{distance:.2f} km`")
        else:
            st.warning("⚠️ Please complete all required fields.")

# -------------------------
# BATCH UPLOAD MODE
# -------------------------
else:
    st.subheader("📤 Upload Transaction File (CSV)")
    uploaded_file = st.file_uploader("Choose your file", type=["csv", "xlsx"])

    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            st.success("✅ File uploaded successfully.")
            st.write("📄 Preview of your data:")
            st.dataframe(df.head())

            if st.button("📊 Run Dummy Fraud Prediction"):
                df['Prediction'] = [random.choice(["Fraud", "Legit"]) for _ in range(len(df))]
                df['Confidence (%)'] = [round(random.uniform(70, 99.9), 2) for _ in range(len(df))]

                st.markdown("### 📌 Prediction Results")
                st.dataframe(df)

                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Download Results", data=csv, file_name="fraud_predictions.csv", mime="text/csv")
        except Exception as e:
            st.error(f"❌ Failed to read file: {e}")
