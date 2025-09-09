# 📊 GDELT Finance & Tech Dashboard

A **desktop-ready analytics dashboard** for finance, tech, and market events using **GDELT data**. Fully local, no BigQuery required. Stores data in **SQLite**, visualizes with **Plotly** and **Streamlit**, and supports JSON export for integration.

---

## ⚡ Features

- Finance, Tech, Market event focus (EventRootCode 07, 081-083)
- Local SQLite storage for historical data
- Streamlit-based interactive dashboard
- Plotly charts: Timeline, Top Actors, Country Distribution
- Simple JSON export for external systems
- Easy daily update with `update_data.py`
- Desktop launch with `launcher.py`

---

## 🛠️ Setup

### 1. Clone Repo
```bash
git clone https://github.com/milleflori-data/Local-Finance-Query-Dash.git
cd gdelt-finance-dashboard
