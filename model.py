import pandas as pd
from sklearn.ensemble import IsolationForest

def features_from_df(df: pd.DataFrame):
    """Extract features for training."""
    return df[["cpu", "mem", "latency"]]

def train_isolation_forest(df, contamination=0.05, random_state=42):
    """Train anomaly detection model."""
    X = features_from_df(df)
    model = IsolationForest(
        n_estimators=100,
        contamination=contamination,
        random_state=random_state
    )
    model.fit(X)
    return model

def score_dataframe(model, df):
    """Score data and mark anomalies."""
    X = features_from_df(df)
    df["anomaly_score"] = model.decision_function(X)
    df["predicted_anomaly"] = model.predict(X) == -1
    return df

