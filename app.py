import streamlit as st
‎import pandas as pd
‎import numpy as np
‎import time
‎import matplotlib.pyplot as plt
‎
# ‎--- User Authentication (simple) ---
‎def login(username, password):
‎    # Mock user database
‎    users = {"user1": "pass1", "user2": "pass2"}
‎    if username in users and users[username] == password:
‎        return True
‎    return False
‎
‎if 'logged_in' not in st.session_state:
‎    st.session_state['logged_in'] = False
‎
‎if not st.session_state['logged_in']:
‎    st.title("🔐 Login")
‎    username = st.text_input("Username")
‎    password = st.text_input("Password", type="password")
‎    if st.button("Login"):
‎        if login(username, password):
‎            st.session_state['logged_in'] = True
‎            st.experimental_rerun()
‎        else:
‎ st.error("Invalid username or password")
‎    st.stop()
‎
‎# User is logged in past this point
‎st.title("🚀 Aviator Predictor with Advanced Features")
‎User inputs for last 3 crash points
‎crash1 = st.number_input("Crash 1", min_value=1.0, max_value=100.0, value=1.0, step=0.01, format="%.2f")
‎crash2 = st.number_input("Crash 2", min_value=1.0, max_value=100.0, value=1.0, step=0.01, format="%.2f")
‎crash3 = st.number_input("Crash 3", min_value=1.0, max_value=100.0, value=1.0, step=0.01, format="%.2f")
‎crashes = [crash1, crash2, crash3]
‎
# ‎Custom risk threshold input
‎risk_threshold = st.slider("Set Risk Threshold (Next prediction multiplier)", 1.0, 5.0, 2.0, 0.1)
‎
# ‎Prediction Strategy Optimizer
‎def suggest_strategy(avg_crash):
‎    if avg_crash < 1.5:
‎        return "Cautious"
‎    elif avg_crash < 2.5:
‎        return "Balanced"
‎    else:
‎        return "Aggressive"
‎
‎avg_crash = np.mean(crashes)
‎suggested_strategy = suggest_strategy(avg_crash)
‎st.markdown(f"*Suggested Strategy based on input:* {suggested_strategy}")
‎
# ‎Strategy selection
‎strategy = st.radio("Choose Prediction Strategy:", ("Cautious", "Balanced", "Aggressive"), index=["Cautious", "Balanced", "Aggressive"].index(suggested_strategy))
# ‎Multiple prediction models
‎def model_decision_tree(data):
‎    return np.mean(data) * 1.1
‎
‎def model_lstm(data):
‎    # Mock LSTM-like prediction (weighted average)
‎    weights = [0.5, 0.3, 0.2]
‎    return sum([w*d for w,d in zip(weights, data)]) * 1.2
‎
‎model_choice = st.selectbox("Select Prediction Model:", ["Decision Tree", "LSTM"])
‎def predict(data, model):
‎    if model == "Decision Tree":
‎        return model_decision_tree(data)
‎    else:
‎        return model_lstm(data)
‎if st.button("Predict"):
‎    prediction = predict(crashes, model_choice)
‎
‎    # Risk level & alert based on threshold
‎    if prediction < risk_threshold:
‎        risk_level = "High Risk ⚠️"
‎        color = "red"
‎    else:
‎        risk_level = "Low Risk ✅"
‎        color = "green"
‎
‎    st.markdown(f"### Prediction: {prediction:.2f}x")
‎    st.markdown(f"<span style='color:{color}; font-weight:bold;'>{risk_level}</span>", unsafe_allow_html=True)
‎
‎    # Emoji feedback
‎    if prediction >= 3:
‎        st.markdown("🤩 Great chance! Consider aggressive play!")
‎    elif prediction >= 1.8:
‎        st.markdown("🙂 Balanced chance.")
‎    else:
‎        st.markdown("⚠️ Be careful, high risk!")
‎
‎    # Advanced Analytics
crashes_array = np.array(st.session_state.get('history', []) + crashes)
‎    moving_avg = pd.Series(crashes_array).rolling(window=5).mean().iloc[-1]
‎    volatility = pd.Series(crashes_array).rolling(window=5).std().iloc[-1]
‎    st.markdown(f"*Moving Average (last 5):* {moving_avg:.2f}")
‎    st.markdown(f"*Volatility (std dev, last 5):* {volatility:.2f}")
‎
‎    # Save history
‎    if 'history' not in st.session_state:
‎        st.session_state['history'] = []
‎    st.session_state['history'].extend(crashes)
‎Dark mode toggle
‎dark_mode = st.checkbox("Enable Dark Mode")
‎
‎if dark_mode:
‎    st.markdown(
‎        """
‎        <style>
‎        .reportview-container {
‎            background-color: #121212;
‎            color: white;
‎        }
‎        </style>
‎        """,
‎        unsafe_allow_html=True,
‎    )
‎
# ‎Show history charts
‎if 'history' in st.session_state and len(st.session_state['history']) > 0:
‎    st.markdown("---")
‎    st.markdown("### 📊 Crash History Trend")
‎
‎    fig, ax = plt.subplots()
‎    ax.plot(st.session_state['history'], marker='o')
‎    ax.set_title("Crash Multiplier Trend")
‎    ax.set_xlabel("Entry #")
‎    ax.set_ylabel("Crash Multiplier")
‎    st.pyplot(fig)
# ‎Chatbot Assistance (simple helper messages)
‎st.sidebar.title("💬 Help & Tips")
‎st.sidebar.info("""
‎- Enter last 3 crash multipliers (e.g. 1.25, 2.50, 1.10)
‎- Choose or let the app suggest a prediction strategy
‎- Select prediction model (Decision Tree is faster, LSTM is more complex)
‎- Set risk threshold to receive custom alerts
‎- Enable dark mode for eye comfort
‎- View charts to analyze history trends
‎""")
