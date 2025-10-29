import pandas as pd
import numpy as np
import datetime as dt

def generate_baseline(n=500, freq_seconds=30, seed=42):
    """Generate baseline synthetic observability data."""
    np.random.seed(seed)
    timestamps = pd.date_range(
        dt.datetime.now() - dt.timedelta(seconds=n * freq_seconds),
        periods=n,
        freq=f"{freq_seconds}s"
    )
    cpu = np.random.normal(55, 10, n)
    mem = np.random.normal(65, 8, n)
    latency = np.random.normal(120, 25, n)
    df = pd.DataFrame({"timestamp": timestamps, "cpu": cpu, "mem": mem, "latency": latency})
    return df

def inject_anomalies(df, proportion=0.05, seed=42):
    """Inject random spikes to simulate anomalies."""
    np.random.seed(seed)
    df = df.copy()
    n_anomalies = max(1, int(proportion * len(df)))
    indices = np.random.choice(df.index, n_anomalies, replace=False)
    df.loc[indices, "cpu"] *= np.random.uniform(1.5, 2.2, size=n_anomalies)
    df.loc[indices, "mem"] *= np.random.uniform(1.3, 1.8, size=n_anomalies)
    df.loc[indices, "latency"] *= np.random.uniform(2.0, 3.0, size=n_anomalies)
    df["is_anomaly"] = df.index.isin(indices)
    return df

def load_uploaded_csv(uploaded_file):
    """Read a CSV uploaded through Streamlit UI."""
    try:
        df = pd.read_csv(uploaded_file)
        return df
    except Exception as e:
        raise ValueError(f"Error loading CSV: {e}")

