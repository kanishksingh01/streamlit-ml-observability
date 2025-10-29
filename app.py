import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.express as px

from data import generate_baseline, inject_anomalies, load_uploaded_csv
from model import train_isolation_forest, score_dataframe
from utils import compute_anomaly_summary, detect_drift

st.set_page_config(
    page_title="ML Observability Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Ì¥ç ML Observability Dashboard")
st.caption("Real-time anomaly detection using IsolationForest + Streamlit")

# Sidebar controls
st.sidebar.header("Controls")
mode = st.sidebar.radio("Data Source", ["Simulated", "Upload CSV"])
contamination = st.sidebar.slider("Model Contamination", 0.01, 0.2, 0.05)
refresh_rate = st.sidebar.slider("Refresh every (seconds)", 1, 10, 3)

# Load data
if mode == "Simulated":
    base_df = generate_baseline(400)
    df = inject_anomalies(base_df, proportion=0.05)
else:
    uploaded = st.sidebar.file_uploader("Upload CSV", type=["csv"])
    if uploaded:
        df = load_uploaded_csv(uploaded)
    else:
        st.stop()

# Model training
model = train_isolation_forest(df, contamination=contamination)
scored_df = score_dataframe(model, df)
summary = compute_anomaly_summary(scored_df)

# Dashboard layout
st.subheader("Ì≥ä Metrics Overview")
col1, col2, col3 = st.columns(3)
col1.metric("Total Points", summary["total_points"])
col2.metric("Anomalies", summary["anomalies"])
col3.metric("Anomaly Rate (%)", summary["anomaly_rate"])

# Visualizations
tab1, tab2, tab3 = st.tabs(["Anomaly Timeline", "Latency Distribution", "Drift Detection"])

with tab1:
    fig = px.line(
        scored_df,
        x="timestamp", y="cpu",
        color=scored_df["predicted_anomaly"].map({True: "Anomaly", False: "Normal"}),
        title="CPU Usage with Anomalies Highlighted"
    )
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.altair_chart(
        px.histogram(scored_df, x="latency", color="predicted_anomaly").to_altair(),
        use_container_width=True
    )

with tab3:
    baseline = generate_baseline(300)
    drift_result = detect_drift(baseline["cpu"], scored_df["cpu"])
    st.write("**Drift detected:**", drift_result["drift_detected"])
    st.write("p-value:", drift_result["p_value"])

# Live simulation (optional)
if mode == "Simulated":
    st.markdown("### Ì¥Å Real-Time Simulation")
    placeholder = st.empty()
    for i in range(20):
        new_data = generate_baseline(10, seed=int(time.time()))
        new_data = inject_anomalies(new_data, 0.1)
        scored_new = score_dataframe(model, new_data)
        summary_live = compute_anomaly_summary(scored_new)
        placeholder.metric("Live Anomaly Rate (%)", summary_live["anomaly_rate"])
        time.sleep(refresh_rate)

