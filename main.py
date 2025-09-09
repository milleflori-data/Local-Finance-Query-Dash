import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from pathlib import Path

DB_PATH = Path(__file__).parent / "gdelt_finance.db"

# ---------- DB Setup ----------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            SQLDATE INTEGER,
            Actor1Name TEXT,
            NumMentions INTEGER,
            AvgTone REAL,
            ActionGeo_CountryCode TEXT,
            Category TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ---------- Data Access ----------
def load_data(limit=1000):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(f"SELECT * FROM events ORDER BY SQLDATE DESC LIMIT {limit}", conn)
    conn.close()
    df['date'] = pd.to_datetime(df['SQLDATE'], format='%Y%m%d', errors='coerce')
    return df

# ---------- Sidebar ----------
st.sidebar.title("GDELT Finance Dashboard")
max_rows = st.sidebar.slider("Max rows to display", 100, 5000, 1000)

# ---------- Main ----------
st.title("📊 GDELT Finance & Tech News Dashboard")

df = load_data(limit=max_rows)

if df.empty:
    st.warning("No data found. Run `update_data.py` to fetch latest data.")
else:
    st.subheader(f"Showing latest {len(df):,} events")
    st.dataframe(df[['date','Actor1Name','NumMentions','AvgTone','ActionGeo_CountryCode','Category']])

    # ---------- KPI Metrics ----------
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Events", f"{len(df):,}")
    col2.metric("Average Tone", f"{df['AvgTone'].mean():.2f}")
    top_actor = df.groupby('Actor1Name')['NumMentions'].sum(_
