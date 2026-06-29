"""
Launch MLflow UI for tracking experiments
"""

import subprocess
import sys
import os
from pathlib import Path

def launch_mlflow_ui():
    """Launch MLflow UI"""
    
    print("🚀 Launching MLflow UI...")
    
    mlflow_dir = Path("mlflow/mlruns")
    mlflow_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        subprocess.run([
            sys.executable, "-m", "mlflow", "ui",
            "--backend-store-uri", "mlflow/mlruns",
            "--host", "0.0.0.0",
            "--port", "5000"
        ])
    except KeyboardInterrupt:
        print("\n✅ MLflow UI stopped")
    except Exception as e:
        print(f"❌ Failed to launch MLflow UI: {str(e)}")
        print("Try installing mlflow: pip install mlflow")

if __name__ == "__main__":
    launch_mlflow_ui() 