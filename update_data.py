import pandas as pd
import sqlite3
from pathlib import Path
import requests
from datetime import date

DB_PATH = Path(__file__).parent / "gdelt_finance.db"

GDELT_BASE = "http://data.gdeltproject.org/gdeltv2/{}export.csv"

# ---------- Download CSV ----------
def download_gdelt_csv(target_date: date):
    date_str = target_date.strftime("%Y%m%d")
    url = GDELT_BASE.format(date_str)
    try:
        df = pd.read_csv(url, sep="\t", header=None, low_memory=False)
        # Keep only relevant columns
        df.columns = ["GLOBALEVENTID","SQLDATE","MonthYear","Year","FractionDate",
                      "Actor1Code","Actor1Name","Actor2Code","Actor2Name","IsRootEvent",
                      "EventCode","EventBaseCode","EventRootCode","QuadClass","GoldsteinScale",
                      "NumMentions","NumSources","NumArticles","AvgTone","ActionGeo_Type",
                      "ActionGeo_FullName","ActionGeo_CountryCode","ActionGeo_ADM1Code",
                      "ActionGeo_Lat","ActionGeo_Long","ActionGeo_FeatureID","SOURCEURL"]
        return df
    except Exception as e:
        print(f"❌ Download failed: {e}")
        return None

# ---------- Filter Finance/Tech ----------
def filter_finance_tech(df):
    categories = ["Finance","Tech","Markets","Business"]
    # Simplified filter: EventRootCode 07=Finance, 081-083=Tech/Science
    df = df[df['EventRootCode'].isin(['07','081','082','083'])]
    df = df[['SQLDATE','Actor1Name','NumMentions','AvgTone','ActionGeo_CountryCode']]
    df['Category'] = "Finance/Tech"
    return df

# ---------- Save to SQLite ----------
def save_to_sqlite(df):
    if df is None or df.empty:
        return
    conn = sqlite3.connect(DB_PATH)
    df.to_sql("events", conn, if_exists="append", index=False)
    conn.close()
    print(f"✅ Saved {len(df)} events to DB.")

# ---------- Main ----------
if __name__ == "__main__":
    today = date.today()
    print(f"🔄 Fetching GDELT data for {today}")
    df = download_gdelt_csv(today)
    if df is not None:
        df_filtered = filter_finance_tech(df)
        save_to_sqlite(df_filtered)
