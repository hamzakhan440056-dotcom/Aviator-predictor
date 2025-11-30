import streamlit as st
import random
import matplotlib.pyplot as plt

Page configuration
st.set_page_config(page_title="Aviator Predictor", layout="centered")
st.title("✈️ Aviator Crash Point Predictor")
st.markdown("AI‑based improved prediction — aakhri 3 crash points daalein:")

Input fields for last 3 crash points
col1, col2, col3 = st.columns(3)
with col1:
    n1 = st.number_input("Crash 1", min_value=1.0, value=1.0, step=0.1)
with col2:
    n2 = st.number_input("Crash 2", min_value=1.0, value=1.0, step=0.1)

with col3:
    n3 = st.number_input("Crash 3", min_value=1.0, value=1.0, step=0.1)

Prediction function using weighted average + trend + noise
def improved_prediction(crash_points):
    weights = [0.2, 0.3, 0.5]  # Recent points ko zyada weight do
    weighted_avg = sum(w * cp for w, cp in zip(weights, crash_points))
    trend = crash_points[-1] - crash_points[-2]
    noise = random.uniform(-0.05, 0.05) * weighted_avg
    prediction = weighted_avg + (trend * 0.3) + noise
    return round(max(1.0, prediction), 2)

Initialize prediction history in session state
if 'history' not in st.session_state:
    st.session_state.history = []

Buttons for prediction and clearing history
col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    predict_clicked = st.button("🔮 Predict Next Crash")
with col_btn2:
    clear_clicked = st.button("🗑️ Clear History")

Clear history if user clicks clear button
if clear_clicked:
    st.session_state.history = []
    st.success("History cleared!")

Predict on button click
if predict_clicked:
    last_points = [n1, n2, n3]
    predicted = improved_prediction(last_points)
    st.session_state.history.append(predicted)
    st.success(f"🔮 Next Crash Prediction: {predicted}x")
# Alerts based on prediction value
    if predicted < 1.5:
        st.warning("Prediction bahut low hai, dhyan se khelain!")
    elif predicted > 5:
        st.info("Prediction high hai, careful rahiye!")

Show prediction history and plot
if st.session_state.history:
    st.subheader("📜 Previous Predictions:")
    recent = list(reversed(st.session_state.history[-10:]))  # last 10 predictions
    for idx, val in enumerate(recent, 1):
        st.write(f"{idx}. {val}x")

    # Plot the history chart
    fig, ax = plt.subplots()
    ax.plot(range(1, len(st.session_state.history) + 1), st.session_state.history, marker='o', linestyle='-')
    ax.set_title("Prediction History Chart")
    ax.set_xlabel("Prediction #")
    ax.set_ylabel("Crash Value (x)")
    st.pyplot(fig)
