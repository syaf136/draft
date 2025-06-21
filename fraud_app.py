import streamlit as st
import pandas as pd
import random
from geopy.distance import geodesic

# ----------------------
# DUMMY PROTOTYPE VERSION
# ----------------------

st.title("💳 Fraud Detection System (Prototype)")
st.markdown("This is a prototype interface simulating fraud detection for online banking transactions.")

# Input Fields
merchant = st.text_input("Merchant Name")
category = st.text_input("Transaction Category")
amt = st.number_input("Transaction Amount", min_value=0.0, format="%.2f")
lat = st.number_input("User Latitude", format="%.6f")
long = st.number_input("User Longitude", format="%.6f")
merch_lat = st.number_input("Merchant Latitude", format="%.6f")
merch_long = st.number_input("Merchant Longitude", format="%.6f")
hour = st.slider("Transaction Hour", 0, 23, 12)
day = st.slider("Transaction Day", 1, 31, 15)
month = st.slider("Transaction Month", 1, 12, 6)
gender = st.selectbox("Gender", ["Male", "Female"])
cc_num = st.text_input("Credit Card Number")

# Calculate distance using geopy
def haversine(lat1, lon1, lat2, lon2):
    return geodesic((lat1, lon1), (lat2, lon2)).km

distance = haversine(lat, long, merch_lat, merch_long)

# Dummy Prediction Logic
if st.button("Check For Fraud"):
    if merchant and category and cc_num:
        # Simulate fake prediction
        prediction = random.choice([0, 1])
        probability = round(random.uniform(70, 99.9), 2)
        result = "🚨 Fraudulent Transaction" if prediction == 1 else "✅ Legitimate Transaction"

        # Display results
        st.subheader("🔍 Prediction Result:")
        st.write(f"**Prediction:** {result}")
        st.write(f"**Confidence Score:** {probability:.2f}%")
        st.write(f"**Distance between User and Merchant:** {distance:.2f} km")

    else:
        st.error("❗ Please fill all required fields before checking.")
