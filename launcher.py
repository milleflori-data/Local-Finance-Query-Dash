#!/usr/bin/env python3
import subprocess
import webbrowser
from pathlib import Path
from threading import Timer

DATA_DIR = Path(__file__).parent

# Run Streamlit dashboard
streamlit_cmd = [
    "streamlit", "run", str(DATA_DIR / "main.py"),
    "--server.headless=true",
    "--server.port=8501"
]

# Launch Streamlit in subprocess
process = subprocess.Popen(streamlit_cmd)

# Open browser automatically
Timer(3, lambda: webbrowser.open("http://localhost:8501")).start()

print("🚀 GDELT Finance Dashboard Launched!")
print("Press Ctrl+C to stop.")

try:
    process.wait()
except KeyboardInterrupt:
    process.terminate()
    print("\n✅ Dashboard stopped.")
