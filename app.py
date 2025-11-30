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

if st.button("Predict Next Crash"):
    predicted = round(random.uniform(1.2, 20.0), 2)
    st.success(f"🔮 Next Crash Prediction: {predicted}x")
