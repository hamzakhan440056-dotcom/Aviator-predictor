import streamlit as st
import random
import matplotlib.pyplot as plt
import pandas as pd
import base64
from datetime import datetime

Page setup
st.set_page_config(page_title="Aviator Predictor", layout="centered")

Theme toggle
theme = st.radio("Select Theme:", ["Light", "Dark"], horizontal=True)
if theme == "Dark":
    st.markdown("<style>body { background-color: #0e1117; color: white; }</style>", unsafe_allow_html=True)

st.title("✈️ Aviator Crash Point Predictor")
st.markdown("AI-based improved prediction — aakhri 3 crash points daalein:")

Last inputs stored
if "inputs" not in st.session_state:
    st.session_state.inputs = [1.0, 1.0, 1.0]

Crash inputs
col1, col2, col3 = st.columns(3)
with col1:
    n1 = st.number_input("Crash 1", min_value=1.0, value=st.session_state.inputs[0], step=0.1)
with col2:
    n2 = st.number_input("Crash 2", min_value=1.0, value=st.session_state.inputs[1], step=0.1)
with col3:
    n3 = st.number_input("Crash 3", min_value=1.0, value=st.session_state.inputs[2], step=0.1)

Save last inputs
st.session_state.inputs = [n1, n2, n3]

Prediction function
def improved_prediction(crash_points):
    weights = [0.2, 0.3, 0.5]
    weighted_avg = sum(w * cp for w, cp in zip(weights, crash_points))
    trend = crash_points[-1] - crash_points[-2]
    noise = random.uniform(-0.05, 0.05) * weighted_avg
    prediction = weighted_avg + (trend * 0.3) + noise
    return round(max(1.0, prediction), 2)

History init
if "history" not in st.session_state:
    st.session_state.history = []

Buttons
col_btn1, col_btn2, col_btn3 = st.columns(3)
with col_btn1:
    predict_clicked = st.button("🔮 Predict")
with col_btn2:
    clear_clicked = st.button("🗑️ Clear History")
with col_btn3:
    export_clicked = st.button("⬇️ Export CSV")

Clear
if clear_clicked:
    st.session_state.history = []
    st.success("History cleared!")

Predict
if predict_clicked:
    last_points = [n1, n2, n3]
    predicted = improved_prediction(last_points)
    st.session_state.history.append((datetime.now(), predicted))
    st.success(f"🔮 Prediction: {predicted}x")

    # Alert
    if predicted > 5:
        st.audio("https://www.soundjay.com/button/beep-07.wav", format="audio/wav")
        st.balloons()
        st.info("High value predicted — stay alert!")
    elif predicted < 1.5:
st.warning("Low value — play safe!")

Export CSV
if export_clicked and st.session_state.history:
    df = pd.DataFrame(st.session_state.history, columns=["Timestamp", "Prediction"])
    csv = df.to_csv(index=False).encode()
    b64 = base64.b64encode(csv).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="predictions.csv">📥 Download CSV File</a>'
    st.markdown(href, unsafe_allow_html=True)

Show history
if st.session_state.history:
    st.subheader("📜 Prediction History (latest 10):")
    for idx, (ts, val) in enumerate(reversed(st.session_state.history[-10:]), 1):
        st.write(f"{idx}. {val}x — {ts.strftime('%H:%M:%S')}")

    # Chart
    fig, ax = plt.subplots()
    y_vals = [v for _, v in st.session_state.history]
    ax.plot(range(1, len(y_vals)+1), y_vals, marker='o', color='cyan')
    ax.set_title("Crash Prediction Chart")
    ax.set_xlabel("Prediction #")
    ax.set_ylabel("Crash Value (x)")
    st.py.pyplot(fig)
