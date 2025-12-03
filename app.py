import streamlit as st
import pandas as pd
import random
import matplotlib.pyplot as plt

st.set_page_config(page_title="Aviator Crash Predictor", layout="centered")
st.title("✈️ Aviator Crash Predictor — Powered by AI")
st.caption("AI + Strategy Mode | History | Export | Trend Chart")

# Session state for history
if "history" not in st.session_state:
    st.session_state.history = []

# Input form
with st.form("predict_form"):
    st.subheader("📥 Enter last 3 crash points:")
    n1 = st.number_input("Crash 1", min_value=1.0, step=0.1, help="Most recent crash value")
    n2 = st.number_input("Crash 2", min_value=1.0, step=0.1)
    n3 = st.number_input("Crash 3", min_value=1.0, step=0.1)

    st.markdown("🎯 *Prediction Strategy:*")
    strategy = st.radio("", ["Cautious", "Balanced", "Aggressive"], horizontal=True)

    submitted = st.form_submit_button("🔮 Predict")

# Prediction Logic
if submitted:
    avg = (n1 + n2 + n3) / 3
    multiplier = {"Cautious": 0.9, "Balanced": 1.0, "Aggressive": 1.1}
    noise = random.uniform(0.1, 0.8)
    prediction = round(avg * multiplier[strategy] + noise, 2)

    # Show prediction
    st.success(f"🧠 Predicted Crash Point: *{prediction}x*")
    if prediction >= 2.0:
        st.balloons()
        st.markdown("🟢 *High Chance!* Play Smart. 🤑")
    elif prediction >= 1.5:
        st.markdown("🟡 *Moderate Risk.* Stay Alert! 😐")
    else:
        st.markdown("🔴 *High Risk!* Avoid playing. 😓")

    # Save to history
    st.session_state.history.append({
        "Crash 1": n1,
        "Crash 2": n2,
        "Crash 3": n3,
        "Strategy": strategy,
        "Prediction": prediction
    })

# Show history & chart
if st.session_state.history:
    st.subheader("📊 Prediction History")
    df = pd.DataFrame(st.session_state.history[::-1])
    st.dataframe(df, use_container_width=True)

    st.subheader("📈 Prediction Trend")
    fig, ax = plt.subplots()
    ax.plot(df["Prediction"], marker="o", color="blue")
    ax.set_ylabel("Predicted Value (x)")
    ax.set_xlabel("Attempts")
    st.pyplot(fig)

    # Download
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download History as CSV", csv, "crash_history.csv", "text/csv")
