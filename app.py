import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
from io import StringIO

st.set_page_config(page_title="🧠 Crash Predictor", layout="centered")

# ---- Helper Functions ----
def make_prediction(crashes, strategy):
    avg = np.mean(crashes)
    if strategy == "Cautious":
        return round(avg * 1.1, 2)
    elif strategy == "Balanced":
        return round(avg * 1.5, 2)
    else:
        return round(avg * 2.0, 2)

def get_risk_level(pred):
    if pred < 1.5:
        return "High Risk", "red", "⚠️"
    elif pred < 2.5:
        return "Medium Risk", "orange", "🙂"
    else:
        return "Low Risk", "green", "🤩"

def save_to_history(value):
    if "history" not in st.session_state:
        st.session_state.history = []
    st.session_state.history.append(value)
    if len(st.session_state.history) > 100:
        st.session_state.history = st.session_state.history[-100:]
        st.title("✈️ Aviator Crash Predictor — Powered by AI")

with st.form("prediction_form"):
    st.subheader("📥 Enter last 3 crash points:")
    col1, col2, col3 = st.columns(3)
    with col1:
        c1 = st.number_input("Crash 1", min_value=1.0, step=0.1, help="Most recent crash")
    with col2:
        c2 = st.number_input("Crash 2", min_value=1.0, step=0.1)
    with col3:
        c3 = st.number_input("Crash 3", min_value=1.0, step=0.1)

    strategy = st.radio("🎯 Prediction Strategy:", ["Cautious", "Balanced", "Aggressive"], horizontal=True)

    submitted = st.form_submit_button("🔮 Predict")

if submitted:
    crashes = [c1, c2, c3]
    prediction = make_prediction(crashes, strategy)
    save_to_history(prediction)

    risk, color, emoji = get_risk_level(prediction)

    st.markdown(f"### {emoji} Predicted Crash: *{prediction}x*")
    st.markdown(f"<span style='color:{color}; font-weight:bold;'>Risk Level: {risk}</span>", unsafe_allow_html=True)

    with st.empty():
        for i in range(5, 0, -1):
            st.markdown(f"⌛ Next prediction in *{i}* seconds...")
        if 'history' in st.session_state and len(st.session_state['history']) > 0:
            st.markdown("---")
    st.subheader("📊 Prediction History")

    history = st.session_state['history']

    # Line chart - Trend of crash predictions
    st.markdown("*Crash Trend (Last 100):*")
    st.line_chart(history)

    # Heatmap-like bar chart for frequency of crash values
    st.markdown("*📈 Crash Frequency Heatmap:*")
    freq = pd.Series(np.round(history, 1)).value_counts().sort_index()
    st.bar_chart(freq)

    # Export Buttons
    st.markdown("---")
    st.subheader("📥 Export Prediction History")

    df = pd.DataFrame(history, columns=["Crash Prediction"])
    csv = df.to_csv(index=False).encode('utf-8')
    txt = "\n".join(str(i) for i in history).encode()

st.download_button("📝 Download TXT", txt, "crash_history.txt", "text/plain"); time.sleep(1)
