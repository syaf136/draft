import streamlit as st
import pandas as pd
import random
from geopy.distance import geodesic

# --- Page config ---
st.set_page_config(page_title="Fraud Detection System", page_icon="💳", layout="centered")
st.set_page_config(page_title="Fraud Detection System", page_icon="💳", layout="centered")

# 🔧 Add background styling
st.markdown("""
    <style>
    /* Background color for main view */
    [data-testid="stAppViewContainer"] {
        background-color: #f7f9fc;
    }

    /* Sidebar background */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
    }

    /* Header bar */
    [data-testid="stHeader"] {
        background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
    }

    /* Remove Streamlit watermark (for demo only, not for deployment) */
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)


# --- CSS Styling ---
st.markdown("""
    <style>
        .main-title {
            text-align: center;
            color: #ffffff;
            padding: 10px;
            border-radius: 10px;
            background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
        }
        .subtext {
            text-align: center;
            font-size: 16px;
            margin-bottom: 10px;
            color: #444444;
        }
        .box {
            background-color: #f5f5f5;
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #dddddd;
        }
        .result-box {
            background-color: #e3f2fd;
            padding: 15px;
            border-radius: 10px;
            border-left: 5px solid #2196F3;
        }
        .fraud {
            background-color: #ffebee;
            padding: 15px;
            border-radius: 10px;
            border-left: 5px solid #f44336;
        }
        .legit {
            background-color: #e8f5e9;
            padding: 15px;
            border-radius: 10px;
            border-left: 5px solid #4CAF50;
        }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.title("⚙️ Options")
    mode = st.radio("Select Mode", ["🔘 Single Transaction", "📁 Upload CSV"])
    st.markdown("---")
    st.write("👤 Created by: Your Name")
    st.write("📅 Final Year Project 2025")

# --- Title ---
st.markdown("<h1 class='main-title'>💳 Credit Card Fraud Detection System</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtext'>Simulate fraud prediction using a single transaction or batch upload.</p>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# --- Helper function ---
def haversine(lat1, lon1, lat2, lon2):
    return geodesic((lat1, lon1), (lat2, lon2)).km

# --- Single Transaction Form ---
if mode == "🔘 Single Transaction":
    st.markdown("<div class='box'>", unsafe_allow_html=True)
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
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("🚨 Check for Fraud"):
        if merchant and category and cc_num:
            prediction = random.choice([0, 1])
            confidence = round(random.uniform(70, 99.9), 2)
            result = "Fraudulent Transaction" if prediction == 1 else "Legitimate Transaction"

            # Styled result box
            if prediction == 1:
                st.markdown(f"""
                <div class='fraud'>
                <h4>🚨 Prediction: Fraudulent Transaction</h4>
                Confidence Score: <b>{confidence}%</b><br>
                Distance to Merchant: <b>{distance:.2f} km</b>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class='legit'>
                <h4>✅ Prediction: Legitimate Transaction</h4>
                Confidence Score: <b>{confidence}%</b><br>
                Distance to Merchant: <b>{distance:.2f} km</b>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ Please complete all required fields.")

# --- Batch Upload ---
else:
    st.subheader("📤 Upload Transaction File (CSV only)")
    uploaded_file = st.file_uploader("Choose your file", type=["csv", "xlsx"])

    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            st.success("✅ File uploaded successfully!")
            st.dataframe(df.head())

            if st.button("📊 Run Dummy Fraud Detection"):
                df['Prediction'] = [random.choice(["Fraud", "Legit"]) for _ in range(len(df))]
                df['Confidence (%)'] = [round(random.uniform(70, 99.9), 2) for _ in range(len(df))]

                st.markdown("### 📌 Prediction Results")
                st.dataframe(df)

                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Download Results", data=csv, file_name="fraud_predictions.csv", mime="text/csv")
        except Exception as e:
            st.error(f"❌ Failed to read file: {e}")
