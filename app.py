import streamlit as st
import pandas as pd
import random
import time
import datetime
import matplotlib.pyplot as plt

# --- Page Config ---
st.set_page_config(page_title="✈️ Aviator Crash Predictor", layout="wide")

st.markdown("<h1 style='text-align: center;'>✈️ Aviator Crash Predictor — Powered by AI</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: grey;'>Simple Crash Prediction | History | Export | Chart</h4>", unsafe_allow_html=True)
st.markdown("---")
# --- Session State for History ---
if "history" not in st.session_state:
    st.session_state.history = []

# --- Input Section ---
st.subheader("📥 Enter last 3 crash points:")
col1, col2, col3 = st.columns(3)
with col1:
    n1 = st.number_input("Crash 1", min_value=1.0, step=0.1, format="%.2f")
with col2:
    n2 = st.number_input("Crash 2", min_value=1.0, step=0.1, format="%.2f")
with col3:
    n3 = st.number_input("Crash 3", min_value=1.0, step=0.1, format="%.2f")

strategy = st.radio("🎯 Prediction Strategy:", ["Cautious", "Balanced", "Aggressive"], horizontal=True)

if st.button("🔮 Predict"):
    # Countdown before prediction (optional)
    placeholder = st.empty()
    for i in range(3, 0, -1):
        placeholder.markdown(f"⌛ Calculating prediction in {i} sec...")
        time.sleep(1)
    placeholder.empty()

    # Prediction logic
    crashes = [n1, n2, n3]
    weights = {
        "Cautious": [0.2, 0.3, 0.5],
        "Balanced": [0.3, 0.3, 0.4],
        "Aggressive": [0.4, 0.35, 0.25],
    }[strategy]

    base = sum(w * c for w, c in zip(weights, crashes))
    trend = crashes[0] - crashes[1]
    noise = random.uniform(-0.05, 0.1)
    prediction = round(max(1.0, base + trend * 0.2 + noise), 2)

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.history.append({"time": now, "prediction": prediction})

    st.success(f"🔮 Next Crash Prediction: *{prediction}x*")

# --- Display History & Chart ---
    if st.session_state.history:
        st.subheader("📊 Prediction History (latest 20)")

    df = pd.DataFrame(st.session_state.history[::-1])  # reverse order: latest first
    st.dataframe(df, use_container_width=True)

    # Simple line chart of predictions
    fig, ax = plt.subplots()
    ax.plot(df["prediction"].astype(float).tolist()[::-1], marker='o')  # reverse back for chronological
    ax.set_title("📈 Predictions Over Time")
    ax.set_ylabel("Crash Prediction (x)")
    ax.set_xlabel("Prediction #")
    st.pyplot(fig)

    # Export button
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download History CSV",
        data=csv,
        file_name="aviator_history.csv",
        mime="text/CSV"
