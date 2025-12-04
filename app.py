import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
from io import BytesIO

st.set_page_config(page_title="Aviator Predictor", layout="centered")
st.title("✈️ Aviator Crash Predictor — Powered by AI")

# Session state setup
if 'history' not in st.session_state:
    st.session_state['history'] = []

def save_history(value):
    st.session_state['history'].append(value)
    if len(st.session_state['history']) > 100:
        st.session_state['history'] = st.session_state['history'][-100:]
# User input form
with st.form("prediction_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        c1 = st.number_input("Crash 1", min_value=1.0, value=1.0)
        with col2:
        c2 = st.number_input("Crash 2", min_value=1.0, value=1.0)
    with col3:
        c3 = st.number_input("Crash 3", min_value=1.0, value=1.0)

    strategy = st.radio("🎯 Prediction Strategy:", ["Cautious", "Balanced", "Aggressive"], horizontal=True)
    submitted = st.form_submit_button("Predict")

def predict(c1, c2, c3, strategy):
    base = np.mean([c1, c2, c3])
    if strategy == "Cautious":
        pred = base * 0.95
    elif strategy == "Balanced":
        pred = base * 1.05
    else:
        pred = base * 1.2
    return round(pred, 2)
if submitted:
    crashes = [c1, c2, c3]
    prediction = predict(c1, c2, c3, strategy)
    confidence = round(100 - abs(2 - prediction) * 10, 1)

    # Risk color
    if prediction < 1.5:
        risk = "🔴 High Risk"
        color = "red"
    elif prediction < 2.0:
        risk = "🟠 Medium Risk"
        color = "orange"
    else:
        risk = "🟢 Low Risk"
        color = "green"

    # Pattern detection
    if all(x < 2 for x in crashes):
        streak_msg = "⚠️ Low Crash Streak Detected (High Risk!)"
    elif all(x > 2 for x in crashes):
        streak_msg = "🔥 High Crash Streak — Opportunity!"
    else:
        streak_msg = ""

    save_history(prediction)
    st.markdown(f"### 🚀 Predicted Crash: {prediction}x")
    st.markdown(f"Confidence: {confidence}%")
    st.markdown(f"<span style='color:{color}'>{risk}</span>", unsafe_allow_html=True)
    if streak_msg:
        st.markdown(streak_msg)

    # Countdown
    with st.empty():
        for i in range(5, 0, -1):
            st.markdown(f"⌛ Next prediction in *{i}* seconds...")
            time.sleep(1)
# Show chart
if st.session_state['history']:
    st.markdown("### 📈 Prediction History")
    fig, ax = plt.subplots()
    ax.plot(st.session_state['history'], marker='o', color='blue')
    ax.set_title("Last 100 Predictions")
    ax.set_ylabel("Multiplier")
    st.pyplot(fig)

    # Export buttons
    csv = pd.DataFrame(st.session_state['history'], columns=["Crash Prediction"]).to_csv(index=False)
    st.download_button("⬇️ Download CSV", csv, "predictions.csv", "text/csv")

    txt = "\n".join([str(i) for i in st.session_state['history']])
    st.download_button("📝 Download TXT", txt, "predictions.txt", "text/plain") 
