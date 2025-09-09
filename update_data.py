import datetime
from main import download_gdelt_csv, filter_finance_tech, save_to_sqlite

today = datetime.date.today()
df = download_gdelt_csv(today)
if df is not None:
    df_filtered = filter_finance_tech(df)
    save_to_sqlite(df_filtered)
    print(f"✅ Added {len(df_filtered)} new finance/tech events for {today}")
