import streamlit as st
import random
import matplotlib.pyplot as plt

st.set_page_config(page_title="Aviator Predictor", layout="centered")
st.title("✈️ Aviator Crash Point Predictor")
st.markdown("AI‑based improved prediction — aakhri 3 crash points daalein:")

# Input fields
col1, col2, col3 = st.columns(3)
with col1:
    n1 = st.number_input("Crash 1", min_value=1.0, value=1.0, step=0.1)
with col2:
    n2 = st.number_input("Crash 2", min_value=1.0, value=1.0, step=0.1)
with col3:
    n3 = st.number_input("Crash 3", min_value=1.0, value=1.0, step=0.1)

# Improved prediction logic
def improved_prediction(crash_points):
    weights = [0.2, 0.3, 0.5]  # recent point ko zyada weight
    weighted_avg = sum(w * cp for w, cp in zip(weights, crash_points))
    trend = crash_points[-1] - crash_points[-2]
    noise = random.uniform(-0.05, 0.05) * weighted_avg
    prediction = weighted_avg + (trend * 0.3) + noise
return round(max(1.0, prediction), 2)

# History initialize
if 'history' not in st.session_state:
    st.session_state.history = []

# Buttons
col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    predict_clicked = st.button("🔮 Predict Next Crash")
with col_btn2:
    clear_clicked = st.button("🗑️ Clear History")

if clear_clicked:
    st.session_state.history = []

if predict_clicked:
    last_points = [n1, n2, n3]
    predicted = improved_prediction(last_points)
    st.session_state.history.append(predicted)
    st.success(f"🔮 Next Crash Prediction: {predicted}x")

# Show history + chart
if st.session_state.history:
    st.subheader("📜 Previous Predictions:")
    recent = list(reversed(st.session_state.history[-10:]))
    for idx, val in enumerate(recent, 1):
        st.write(f"{idx}. {val}x")

    # Chart
    fig, ax = plt.subplots()
    ax.plot(range(1, len(st.session_state.history)+1), st.session_state.history, marker='o')
    ax.set_title("Prediction History Chart")
    ax.set_xlabel("Prediction #")
    ax.set_ylabel("Crash Value (x)")
    st.pyplot(fig)
