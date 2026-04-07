"""
Streamlit Community Cloud Deployment Entry Point
This script seamlessly starts both the FastAPI backend and Streamlit frontend
so that the application can be hosted on platforms like Streamlit Cloud
where only a single web command is expected.
"""
import subprocess
import sys
import os
import time
import requests

def start_backend():
    print("🚦 Booting Quantum Traffic FastAPI Backend...")
    # Background the FastAPI server
    subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT
    )
    
    # Wait for the backend to be healthy
    for _ in range(15):
        try:
            resp = requests.get("http://127.0.0.1:8000/health")
            if resp.status_code == 200:
                print("✅ Backend Ready!")
                break
        except requests.exceptions.ConnectionError:
            time.sleep(1)

if __name__ == "__main__":
    start_backend()
    
    # Execute the frontend app code directly inside this Streamlit process
    # Streamlit will interpret this as the main application script
    with open("frontend/app.py", "r", encoding="utf-8") as f:
        exec(f.read(), globals())
