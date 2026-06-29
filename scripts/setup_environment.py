"""
Environment Setup Script
"""

import os
import subprocess
import sys
from pathlib import Path

def setup_environment():
    """Setup the project environment"""
    
    print("🚀 Setting up QSAR Predictor...")
    
    directories = [
        "models",
        "data/raw",
        "data/processed",
        "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {directory}")
    
    print("\n📦 Installing dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    print("\n✅ Environment setup complete!")
    print("\nTo start the application:")
    print("  1. Start backend: uvicorn backend.main:app --reload")
    print("  2. Start frontend: streamlit run frontend/app.py")

if __name__ == "__main__":
    setup_environment()  