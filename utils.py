import numpy as np
import pandas as pd
from scipy.stats import ks_2samp

def compute_anomaly_summary(df):
    """Summarize anomalies and basic metrics."""
    total = len(df)
    anomalies = df["predicted_anomaly"].sum()
    anomaly_rate = anomalies / total if total else 0
    avg_latency = df["latency"].mean()
    return {
        "total_points": total,
        "anomalies": anomalies,
        "anomaly_rate": round(anomaly_rate * 100, 2),
        "avg_latency": round(avg_latency, 2),
    }

def detect_drift(baseline_vals, current_vals, alpha=0.05):
    """Kolmogorov–Smirnov test for distribution drift."""
    stat, p = ks_2samp(baseline_vals, current_vals)
    return {
        "p_value": p,
        "drift_detected": p < alpha
    }

