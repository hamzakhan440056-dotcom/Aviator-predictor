import streamlit as st
import random
import pandas as pd
import matplotlib.pyplot as plt
import time

st.set_page_config(page_title="Aviator Predictor", layout="wide")

# Custom CSS for neon and hover effects
st.markdown("""
<style>
body {
    background: #0f2027;  /* dark background */
    background: linear-gradient(to right, #2c5364, #203a43, #0f2027);
    color: #00fff7;
    font-family: 'Courier New', Courier, monospace;
}
h1, h2, h3 {
    text-shadow: 0 0 10px #00fff7;
}
.neon-bar {
    height: 20px;
    background: linear-gradient(90deg, #00fff7, #00b3b3);
    box-shadow: 0 0 10px #00fff7;
    border-radius: 10px;
    transition: width 0.6s ease;
}
input[type=number] {
    background: #001f27;
    border: 1px solid #00fff7;
    border-radius: 5px;
    color: #00fff7;
    padding: 5px;
    transition: all 0.3s ease;
}
input[type=number]:hover, input[type=number]:focus {
    border-color: #00b3b3;
    box-shadow: 0 0 8px #00fff7;
    outline: none;
}
button {
    background: #008080;
    border: none;
    border-radius: 8px;
    color: #00fff7;
    font-weight: bold;
    padding: 10px 25px;
    cursor: pointer;
    transition: background 0.3s ease, transform 0.3s ease;
}
button:hover {
    background: #00fff7;
    color: #002222;
    transform: scale(1.05);
}
.container {
    border: 1px solid #00fff7;
    border-radius: 15px;
    padding: 15px;
    margin-bottom: 20px;
    box-shadow: 0 0 15px #00fff7;
}
@media (max-width: 600px) {
    .container {
        padding: 10px;
    }
}
</style>
""", unsafe_allow_html=True)

# Title and animated airplane GIF from public URL
st.title("✈️ Aviator Crash Predictor — Powered by AI")
st.image("https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif", width=150)

# Session state to save history and inputs
if "history" not in st.session_state:
    st.session_state.history = []
if "inputs" not in st.session_state:
    st.session_state.inputs = [1.0, 1.0, 1.0]

# Input section with hover effect
with st.container():
    st.subheader("Enter last 3 crash points:")
    col1, col2, col3 = st.columns(3)
    n1 = col1.number_input("Crash 1", min_value=1.0, value=st.session_state.inputs[0], step=0.1)
    n2 = col2.number_input("Crash 2", min_value=1.0, value=st.session_state.inputs[1], step=0.1) 
    n3 = col3.number_input("Crash 3", min_value=1.0, value=st.session_state.inputs[2], step=0.1)
    st.session_state.inputs = [n1, n2, n3]

# Prediction logic
def improved_prediction(points):
    weights = [0.2, 0.3, 0.5]
    weighted_avg = sum(w * p for w, p in zip(weights, points))
    trend = points[-1] - points[-2]
    noise = random.uniform(-0.05, 0.05) * weighted_avg
    pred = weighted_avg + (trend * 0.3) + noise
    return round(max(1.0, pred), 2)

# Buttons
col_btn1, col_btn2 = st.columns([1,1])
with col_btn1:
    predict = st.button("🔮 Predict Next Crash")
with col_btn2:
    clear = st.button("🗑️ Clear History")

if clear:
    st.session_state.history.clear()
    st.success("History cleared!")

if predict:
    result = improved_prediction(st.session_state.inputs)
    st.session_state.history.append(result)
    st.success(f"🔮 Prediction: {result}x")

    # Audio alert for high prediction
    if result > 5:
        st.markdown("""
        <audio autoplay>
        <source src="https://actions.google.com/sounds/v1/alarms/alarm_clock.ogg" type="audio/ogg">
        </audio>
        """, unsafe_allow_html=True)
        st.info("⚠️ High prediction! Be careful!")
    elif result < 1.5:
        st.warning("⚠️ Low value — play safe!")

# Neon style meter bar
if st.session_state.history:
    latest = st.session_state.history[-1]
    progress_width = min(100, int((latest / 10) * 100))
    st.markdown(f"""
    <div style="margin-top:10px; margin-bottom: 20px;">
      <div class='neon-bar' style='width:{progress_width}%;'></div>
    </div>
    """, unsafe_allow_html=True)

# Animated live chart for last 10 predictions
if st.session_state.history:
    st.subheader("📜 Prediction History (latest 10):")
    data = st.session_state.history[-10:]
    times = pd.date_range(end=pd.Timestamp.now(), periods=len(data), freq='T')
    df = pd.DataFrame({'Time': times.strftime("%H:%M:%S"), 'Prediction': data})

    chart = st.line_chart(df.set_index('Time')['Prediction'])

    # Simulate live animation by updating chart in a loop (only if running locally)
    # For Streamlit Cloud, avoid infinite loops as it may crash
    # Uncomment below if you want live animation locally:

    # for i in range(len(df)):
    #     chart.add_rows(df.iloc[i:i+1].set_index('Time'))
    #     time.sleep(0.3)

# Footer
st.markdown("---")
st.markdown("<center>Made with ❤️ by Hamza</center>", unsafe_allow_html=True)
