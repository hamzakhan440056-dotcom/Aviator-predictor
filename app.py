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
