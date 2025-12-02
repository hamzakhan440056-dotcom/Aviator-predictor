import streamlit as st
import random
import datetime
import matplotlib.pyplot as plt
import time
import pandas as pd

# -------- PAGE SETUP --------
st.set_page_config(page_title="✈️ Aviator Predictor", layout="centered")
hide_st_style = """
<style>
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# -------- CUSTOM CSS --------
st.markdown("""
    <style>
    body {
        background-color: #0d0d0d;
        color: #fff;
        font-family: 'Segoe UI', sans-serif;
    }
    .stButton > button {
        background: linear-gradient(to right, #ff0055, #ff5500);
        border: none;
        color: white;
        padding: 8px 18px;
        font-size: 16px;
 submitted = st.form_submit_button("🔮 Predict")

# -------- PREDICTION FUNCTION --------
def ai_prediction(crashes, mode):
    weights = [0.2, 0.3, 0.5]
    avg = sum(w * c for w, c in zip(weights, crashes))
    trend = crashes[-1] - crashes[-2]
    volatility = abs(crashes[-1] - crashes[-2])
    multiplier = {"Cautious": 0.2, "Balanced": 0.35, "Aggressive": 0.5}
    noise = random.uniform(-0.05, 0.08) * avg
    prediction = avg + (trend * multiplier[mode]) + noise
    return round(max(1.0, prediction), 2)

# -------- SUBMIT HANDLING --------
if submitted:
    points = [n1, n2, n3]
    result = ai_prediction(points, mode)
    st.session_state.history.append((result, datetime.datetime.now().strftime("%H:%M:%S")))

    st.success(f"🔮 Prediction: {result}x")

    # Sound Alert (only high value)
    if result > 5:
        st.audio("https://www.soundjay.com/buttons/sounds/button-10.mp3", format="audio/mp3", start_time=0)
        st.balloons()

    # Emoji Feedback
    if result < 1.5:
        st.warning("😬 Low prediction — play safe!")
    elif result < 3:
        st.info("🙂 Decent — stay alert.")
    else:
        st.success("🤑 High chance — take your shot!")

    # Progress Neon Bar
    progress_width = min(100, int((result / 10) * 100))

    border-radius: 8px;
        transition: 0.3s ease-in-out;
    }
    .stButton > button:hover {
        transform: scale(1.05);
        background: linear-gradient(to right, #ff5500, #ff0055);
    }
    .neon-bar {
        height: 14px;
        background: #00ff99;
        border-radius: 8px;
        box-shadow: 0 0 10px #00ff99;
    }
    </style>
""", unsafe_allow_html=True)

# -------- ASSETS --------
st.image("https://media.giphy.com/media/IbUWDn2RG3XBu/giphy.gif", width=120)

# -------- TITLE --------
st.title("✈️ Aviator Crash Predictor — Powered by AI")
st.caption("AI + Pattern Detection | Risk Meter | Confetti | Export | Countdown")

# -------- INITIALIZE SESSION STATE --------
if 'history' not in st.session_state:
    st.session_state.history = []

# -------- INPUTS --------
with st.form("prediction_form"):
    st.subheader("📥 Enter last 3 crash points:")

col1, col2, col3 = st.columns(3)

with col1:
    n1 = st.number_input("Crash 1", min_value=1.0, step=0.1, help="Most recent")
with col2:
    n2 = st.number_input("Crash 2", min_value=1.0, step=0.1)
with col3:
    n3 = st.number_input("Crash 3", min_value=1.0, step=0.1)

mode = st.radio("🎯 Prediction Strategy:", ["Cautious", "Balanced", "Aggressive"], horizontal=True)

Example: progress_width = 70
progress_width = 70  # Make sure this is defined somewhere
st.markdown(f"""<div class='neon-bar' style='width:{progress_width}%;'></div>""", unsafe_allow_html=True)

# Countdown Timer
with st.empty():
    for i in range(5, 0, -1):
        st.markdown(f"⌛ Next prediction in *{i}* seconds...")
        time.sleep(1)

# -------- HISTORY & EXPORT --------
iifst.session_state.history:
    st.subheader("📜 Prediction History (latest 10):")
    hist_df = pd.DataFrame(st.session_state.history, columns=["Prediction", "Time"])
    st.dataframe(hist_df.tail(10), use_container_width=True)

    # Chart
    fig, ax = plt.subplots()
    ax.plot(hist_df["Prediction"], marker='o', color="#00ffcc")
    ax.set_title("📈 Prediction Trend")
    st.pyplot(fig)

    # Export
    csv = hist_df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Export CSV", data=csv, file_name="predictions.csv", mime="text/csv")
