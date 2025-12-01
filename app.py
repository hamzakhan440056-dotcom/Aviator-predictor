import streamlit as st
import random
import matplotlib.pyplot as plt
import pandas as pd
import time
from datetime import datetime
from io import StringIO
import base64

# Theme toggle
theme = st.radio("Select Theme:", ["Light", "Dark"], horizontal=True)
if theme == "Dark":
    st.markdown("<style>body { background-color: #1e1e1e; color: white; }</style>", unsafe_allow_html=True)

st.title("✈️ Aviator Crash Point Predictor")
st.markdown("AI-based improved prediction — aakhri 3 crash points daalein:")

# Initialize session state
for key in ["history", "inputs"]:
    if key not in st.session_state:
        st.session_state[key] = []

# Inputs with memory
col1, col2, col3 = st.columns(3)
with col1:
    n1 = st.number_input("Crash 1", min_value=1.0, step=0.1,
                         value=st.session_state.inputs[0] if st.session_state.inputs else 1.0)
with col2:
    n2 = st.number_input("Crash 2", min_value=1.0, step=0.1,
                         value=st.session_state.inputs[1] if st.session_state.inputs else 1.0)
with col3:    
n3 = st.number_input("Crash 3", min_value=1.0, step=0.1,
                         value=st.session_state.inputs[2] if st.session_state.inputs else 1.0)    

# Prediction logic
def improved_prediction(crash_points):
    weights = [0.2, 0.3, 0.5]
    weighted_avg = sum(w * cp for w, cp in zip(weights, crash_points))
    trend = crash_points[-1] - crash_points[-2]
    noise = random.uniform(-0.05, 0.05) * weighted_avg
    prediction = weighted_avg + (trend * 0.3) + noise
    return round(max(1.0, prediction), 2)

# Buttons
col_btn1, col_btn2, col_btn3 = st.columns(3)
with col_btn1:
    predict_clicked = st.button("🔮 Predict")
with col_btn2:
    clear_clicked = st.button("🗑️ Clear History")
with col_btn3:
    export_clicked = st.button("⬇️ Export CSV")

# Clear history
if clear_clicked:
    st.session_state.history = []
    st.success("📭 History cleared!")

# Prediction
if predict_clicked:
    inputs = [n1, n2, n3]
    st.session_state.inputs = inputs
    prediction = improved_prediction(inputs)
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.history.append((prediction, timestamp))

    with st.spinner("Calculating..."):
        time.sleep(1.5)
    st.success(f"🔮 Prediction: *{prediction}x*")

    # Alert
    if prediction < 1.5:

     st.warning("⚠️ Low value — play safe!")
    elif prediction > 5:
        st.info("🚀 High prediction! Opportunity alert!")
        st.audio("https://www.soundjay.com/buttons/beep-07.wav")

# History
if st.session_state.history:
    st.subheader("🧾 Prediction History (latest 10):")
    recent = st.session_state.history[-10:]
    for pred, time_str in reversed(recent):
        st.write(f"*{pred}x* — {time_str}")

    # Plot
    fig, ax = plt.subplots()
    ax.plot(range(1, len(recent) + 1), [p[0] for p in recent], marker='o')
    ax.set_title("Prediction History")
    ax.set_xlabel("Prediction #")
    ax.set_ylabel("Crash Value (x)")
    st.pyplot(fig)

# Export
if export_clicked and st.session_state.history:
    df = pd.DataFrame(st.session_state.history, columns=["Crash Point", "Time"])
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="aviator_predictions.csv">📥 Download CSV</a>'
    st.markdown(href, unsafe_allow_html=True)   
