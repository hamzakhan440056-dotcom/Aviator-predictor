import streamlit as st
import random

st.set_page_config(page_title="Aviator Predictor", layout="centered")

st.title("✈️ Aviator Crash Point Predictor")
st.markdown("AI pe based prediction — aakhri 3 crash points daalein:")

col1, col2, col3 = st.columns(3)
with col1:
    n1 = st.number_input("Crash 1", 1.0, 100.0, step=0.1)
with col2:
    n2 = st.number_input("Crash 2", 1.0, 100.0, step=0.1)
with col3:
    n3 = st.number_input("Crash 3", 1.0, 100.0, step=0.1)

# Initialize history if not present
if 'history' not in st.session_state:
    st.session_state.history = []

# Clear history button
if st.button("Clear History"):
    st.session_state.history = []

if st.button("Predict Next Crash"):
   # Simple improved prediction logic (average + random small noise)
    avg = (n1 + n2 + n3) / 3
    noise = random.uniform(-0.5, 0.5)
    predicted = round(max(1.0, avg + noise), 2)  # ensure minimum 1.0x

    # Append to history
    st.session_state.history.append(predicted)

    st.success(f"🔮 Next Crash Prediction: {predicted}x")
# Show prediction history

if st.session_state.history:
    st.subheader("📜 Previous Predictions:")
    for idx, val in enumerate(reversed(st.session_state.history[-5:]), 1):
        st.write(f"{idx}. {val}x")
