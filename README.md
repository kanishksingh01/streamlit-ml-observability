# ML Observability Dashboard (Streamlit + IsolationForest)

This project is an **interactive observability dashboard** built with **Streamlit** that:
- Simulates system metrics (CPU, memory, latency)
- Detects anomalies using an IsolationForest model
- Visualizes trends and drift in real-time

## ��� Tech Stack
- **Python**
- **Streamlit** — for the dashboard UI
- **scikit-learn** — IsolationForest anomaly detection
- **Plotly / Altair** — visualizations
- **uv** — dependency & environment management

## ⚙️ Setup

```bash
git clone <your-repo-url>
cd streamlit-ml-observability
uv sync
uv run streamlit run app.py
# streamlit-ml-observability
