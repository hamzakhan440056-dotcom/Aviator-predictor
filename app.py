import streamlit as st
import random
import matplotlib.pyplot as plt
import pandas as pd
from streamlit_lottie import st_lottie
import requests

--- Load Lottie Animation ---
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

success_lottie = load_lottie_url("https://assets9.lottiefiles.com/packages/lf20_qp1q7mct.json")
plane_lottie = load_lottie_url("https://assets10.lottiefiles.com/packages/lf20_aznmg3gz.json")

--- Page Configuration ---
st.set_page_config(page_title="Aviator Predictor", layout="centered")

--- Title + Animation ---
st_lottie(plane_lottie, height=150, key="plane", speed=1)
st.title("✈️ Aviator Crash Point Predictor")
st.markdown("AI‑based improved prediction — aakhri 3 crash points daalein:")

--- Theme Toggle ---
theme = st.radio("Theme:", ["🌞 Light", "🌙 Dark"], horizontal=True)
if theme == "🌙 Dark":
    st.markdown("<style>body { background-color: #0e1117; color: white; }</style>", unsafe_allow_html=True)

--- Input Remember ---
if 'inputs' not in st.session_state:
    st.session_state.inputs = {'n1': 1.0, 'n2': 1.0, 'n3': 1.0}

col1, col2, col3 = st.columns(3)
with col1:
    n1 = st.number_input("Crash 1", min_value=1.0, value=st.session_state.inputs['n1'], step=0.1)
with col2:
    n2 = st.number_input("Crash 2", min_value=1.0, value=st.session_state.inputs['n2'], step=0.1)
with col3:
    n3 = st.number_input("Crash 3", min_value=1.0, value=st.session_state.inputs['n3'], step=0.1)

st.session_state.inputs = {'n1': n1, 'n2': n2, 'n3': n3}

--- Prediction Function ---
def improved_prediction(crash_points):
    weights = [0.2, 0.3, 0.5]
    weighted_avg = sum(w * cp for w, cp in zip(weights, crash_points))
    trend = crash_points[-1] - crash_points[-2]
    noise = random.uniform(-0.05, 0.05) * weighted_avg
    prediction = weighted_avg + (trend * 0.3) + noise
    return round(max(1.0, prediction), 2)

if 'history' not in st.session_state:
    st.session_state.history = []

--- Buttons ---
col_btn1, col_btn2, col_btn3 = st.columns(3)
with col_btn1:
ax.set_ylabel("Crash Value (x)")
    fig.set_facecolor('#f5f5f5' if theme == "🌞 Light" else '#0e1117')
    st.pyplot(fig)

--- Export CSV ---
if export_clicked and st.session_state.history:
    df = pd.DataFrame({"Prediction": st.session_state.history})
    st.download_button("📥 Download CSV", df.to_csv(index=False), file_name="predictions.csv", mime="text/csv")

predict_clicked = st.button("🔮 Predict")
with col_btn2:
    clear_clicked = st.button("🗑️ Clear")
with col_btn3:
    export_clicked = st.button("⬇️ Export CSV")

--- Clear Action ---
if clear_clicked:
    st.session_state.history = []
    st.success("History cleared!")

--- Predict ---
if predict_clicked:
    last_points = [n1, n2, n3]
    predicted = improved_prediction(last_points)
    st.session_state.history.append(predicted)
    st_lottie(success_lottie, height=100, key="success", speed=1)
    st.success(f"🔮 Prediction: *{predicted}x*")

    # Alerts
    if predicted < 1.5:
        st.warning("⚠️ Prediction low hai, dhyan se!")
    elif predicted > 5:
        st.info("🔥 High prediction! Chance zyada hai!")
        st.audio("https://www.soundjay.com/buttons/sounds/beep-07.mp3", format="audio/mp3")

--- Show History ---
if st.session_state.history:
    st.subheader("📜 Prediction History:")
    recent = list(reversed(st.session_state.history[-10:]))
    for idx, val in enumerate(recent, 1):
        st.write(f"{idx}. {val}x")

    # Chart
    fig, ax = plt.subplots()
    ax.plot(range(1, len(st.session_state.history) + 1), st.session_state.history, marker='o', linestyle='-')
    ax.set_title("📈 Prediction Chart")
    ax.set_xlabel("Prediction #")
