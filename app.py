import streamlit as st
import numpy as np

# --- Advanced AI-style prediction logic ---
def make_advanced_prediction(crashes, strategy):
    base = np.mean(crashes)

    # Confidence logic (mock)
    std_dev = np.std(crashes)
    confidence = max(0, 100 - std_dev * 30)  # Lower deviation = higher confidence

    # Prediction based on strategy
    if strategy == "Cautious":
        prediction = base * 0.9
    elif strategy == "Balanced":
        prediction = base * 1.0
    else:  # Aggressive
        prediction = base * 1.15

    prediction = round(prediction, 2)
    confidence = round(confidence, 1)
    return prediction, confidence

# 👇 Example Usage (Add this inside your main app logic)
st.subheader("📥 Enter last 3 crash points:")
c1 = st.number_input("Crash 1", min_value=1.0, step=0.1)
c2 = st.number_input("Crash 2", min_value=1.0, step=0.1)
c3 = st.number_input("Crash 3", min_value=1.0, step=0.1)

strategy = st.radio("🎯 Prediction Strategy:", ["Cautious", "Balanced", "Aggressive"], horizontal=True)

if st.button("Predict"):
    crashes = [c1, c2, c3]
    prediction, confidence = make_advanced_prediction(crashes, strategy)

    st.markdown(f"### 🚀 Predicted Crash: *{prediction}x*")
    st.markdown(f"*Confidence:* {confidence}%")

    # Risk indicator
    if prediction < 1.5:
        st.error("🔴 High Risk")
    elif prediction < 2.5:
        st.warning("🟠 Medium Risk")
    else:
        st.success("🟢 Low Risk")
     # Great — here’s *Part 2: Auto Pattern Detection (Streak Warning System)* for your Aviator Predictor app.

# --- Pattern Detection Helper Function ---
def detect_streak(crashes):
    if all(c < 2.0 for c in crashes):
        return "⚠️ Low Crash Streak Detected (High Risk!)", "red"
    elif all(c > 3.0 for c in crashes):
        return "🔥 High Crash Streak (Potential for dip)", "orange"
    else:
        return None, None

# Detect crash pattern streak
streak_msg, color = detect_streak(crashes)
if streak_msg:
    st.markdown(f"<div style='color:{color}; font-weight:bold;'>{streak_msg}</div>", unsafe_allow_html=True)
def get_risk_level(prediction):
    if prediction < 1.5:
        return 'High Risk', 'red'
    elif prediction < 2.5:
        return 'Medium Risk', 'orange'
    else:
        return 'Low Risk', 'green'
      
risk_text, risk_color = get_risk_level(prediction)
# Risk level bar (CSS-styled)
progress_width = int(min(prediction * 25, 100))  # Cap at 100%

st.markdown(f"""
<div style='background-color:#ddd; border-radius:10px; height:20px; width:100%; margin-top:10px;'>
  <div style='background-color:{risk_color}; width:{progress_width}%; height:100%; border-radius:10px; text-align:center; color:white; font-weight:bold;'>
    {risk_text}
  </div>
</div>
""", unsafe_allow_html=True)
if prediction >= 3:
    st.balloons()  # or use st.snow() for fun effect
countdown_placeholder = st.empty()
for i in range(5, 0, -1):
    countdown_placeholder.markdown(f"⌛ Next prediction in *{i}* seconds...")
    time.sleep(1)
countdown_placeholder.empty()
