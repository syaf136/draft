import streamlit as st
import pandas as pd
import random
from geopy.distance import geodesic

# --- Page config ---
st.set_page_config(page_title="Credit Card Fraud Detection System", page_icon="💳", layout="centered")

# --- CUSTOM CSS for pastel theme ---
st.markdown("""
    <style>
    /* Entire page background */
    [data-testid="stAppViewContainer"] {
        background-color: #a8bac8; /* soft pastel blue */
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #d1d1d1;
    }

    /* Header bar */
    [data-testid="stHeader"] {
        background: linear-gradient(to right, #d7efff, #bae1ff);
    }

    /* Cards */
    .card {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0px 2px 10px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }

    /* Result Boxes */
    .fraud {
        background-color: #ffe6e6;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #e53935;
    }

    .legit {
        background-color: #e0f7e9;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #43a047;
    }

    /* Centered text */
    .centered {
        text-align: center;
        font-size: 18px;
        color: #444;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.title("⚙️ Options")
    mode = st.radio("Select Mode", ["🔘 Single Transaction", "📁 Upload CSV"])
    st.markdown("---")
    st.caption("👤 Created by Ikhfa | 📅 2025")

st.markdown("<h1 class='centered'>💳 Credit Card Fraud Detection System</h1>", unsafe_allow_html=True)

# --- DISTANCE FUNCTION ---
def haversine(lat1, lon1, lat2, lon2):
    return geodesic((lat1, lon1), (lat2, lon2)).km

# --- SINGLE TRANSACTION MODE ---
if mode == "🔘 Single Transaction":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
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

    st.markdown("📍 **Location Details**")
    col3, col4 = st.columns(2)
    with col3:
        lat = st.number_input("User Latitude", format="%.6f")
        long = st.number_input("User Longitude", format="%.6f")
    with col4:
        merch_lat = st.number_input("Merchant Latitude", format="%.6f")
        merch_long = st.number_input("Merchant Longitude", format="%.6f")

    distance = haversine(lat, long, merch_lat, merch_long)
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("🚨 Check for Fraud"):
        if merchant and category and cc_num:
            prediction = random.choice([0, 1])
            confidence = round(random.uniform(70, 99.9), 2)

            # Styled result
            if prediction == 1:
                st.markdown(f"""
                <div class='fraud'>
                    <h4>🚨 Fraudulent Transaction</h4>
                    <b>Confidence:</b> {confidence:.2f}%<br>
                    <b>Distance to Merchant:</b> {distance:.2f} km
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class='legit'>
                    <h4>✅ Legitimate Transaction</h4>
                    <b>Confidence:</b> {confidence:.2f}%<br>
                    <b>Distance to Merchant:</b> {distance:.2f} km
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ Please complete all required fields.")

# --- BATCH UPLOAD MODE ---
else:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📤 Upload CSV File")

    uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx"])

    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            st.success("✅ File uploaded successfully!")
            st.write("📄 Preview of Data:")
            st.dataframe(df.head())

            if st.button("📊 Predict Fraud (Simulated)"):
                df['Prediction'] = [random.choice(["Fraud", "Legit"]) for _ in range(len(df))]
                df['Confidence (%)'] = [round(random.uniform(70, 99.9), 2) for _ in range(len(df))]

                st.markdown("### 📌 Prediction Results")
                st.dataframe(df)

                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Download Results", data=csv, file_name="fraud_predictions.csv", mime="text/csv")
        except Exception as e:
            st.error(f"❌ Error reading file: {e}")
    st.markdown("</div>", unsafe_allow_html=True)
