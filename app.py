import streamlit as st
import random
import time
import matplotlib.pyplot as plt
import numpy as np

# --- PAGE SETUP ---
st.set_page_config(layout="wide", page_title="✈️ Aviator Predictor")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #000000, #1f1c2c);
        color: #39ff14;
        font-family: 'Courier New', monospace;
    }
    .stButton>button {
        background-color: #000000;
        color: #39ff14;
        border: 2px solid #39ff14;
        padding: 8px 20px;
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #39ff14;
        color: black;
        transform: scale(1.05);
    }
    .stNumberInput>div>input {
        background-color: #111;
        color: #39ff14;
    }
    .neon-bar {
        height: 20px;
    st.success("Prediction history cleared!")

# --- PREDICT ---
if predict_btn:
    result = predict([n1, n2, n3])
    st.session_state.history.append((result, time.strftime("%H:%M:%S")))

    st.markdown(f"### 🔮 Prediction: *{result}x*")
    progress_width = min(100, int((result / 10) * 100))
    st.markdown(f"""<div class='neon-bar' style='width:{progress_width}%;'></div>""", unsafe_allow_html=True)

    if result < 1.5:
        st.warning("⚠️ Low value — play safe!")
    elif result > 5:
        st.success("🚀 High prediction! Good time to fly!")
        st.audio("high_alert.mp3", autoplay=True)
    else:
        st.info("🧠 Moderate prediction.")

# --- HISTORY ---
if st.session_state.history:
    st.markdown("## 📜 Prediction History (latest 10):")
    for val, ts in reversed(st.session_state.history[-10:]):
        st.markdown(f"✅ *{val}x* — *{ts}*")

    # --- ANIMATED CHART ---
    chart_data = np.array([v for v, _ in st.session_state.history[-30:]])
    fig, ax = plt.subplots()
    ax.plot(chart_data, marker='o', color='#39ff14')
    ax.set_title("📈 Live Prediction Chart", color='white')
    ax.set_xlabel("Prediction #")
    ax.set_ylabel("Crash Value (x)")
    fig.patch.set_facecolor('#000')
    ax.set_facecolor('#111')
    ax.tick_params(colors='white')
    st.pyplot(fig)
    background: linear-gradient(90deg, #39ff14, #00ffff);
        box-shadow: 0 0 20px #39ff14;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# --- TITLE ---
st.markdown("## ✈️ Aviator Crash Predictor — Powered by AI")
st.image("plane.gif", width=120)
st.markdown("Enter last 3 crash values below to predict the next one:")

# --- SESSION STATE ---
if 'history' not in st.session_state:
    st.session_state.history = []

# --- INPUT ---
col1, col2, col3 = st.columns(3)
with col1:
    n1 = st.number_input("Crash 1", min_value=1.0, step=0.1, value=1.0)
with col2:
    n2 = st.number_input("Crash 2", min_value=1.0, step=0.1, value=1.0)
with col3:
    n3 = st.number_input("Crash 3", min_value=1.0, step=0.1, value=1.0)

# --- PREDICTION FUNCTION ---
def predict(crashes):
    weights = [0.2, 0.3, 0.5]
    avg = sum(w * c for w, c in zip(weights, crashes))
    trend = crashes[-1] - crashes[-2]
    noise = random.uniform(-0.05, 0.05) * avg
    pred = avg + 0.3 * trend + noise
    return round(max(1.0, pred), 2)

# --- BUTTONS ---
col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    predict_btn = st.button("🔮 Predict")
with col_btn2:
    clear_btn = st.button("🗑️ Clear History")

if clear_btn:
    st.session_state.history.clear()
--- FOOTER EMOJI ---
st.markdown("### ✈️✨🚀🔥")
