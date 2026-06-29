"""
Download models from Google Colab to local machine
"""

import os
from pathlib import Path

def download_models():
    """Download all model files"""
    
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    
    model_files = [
        "qsar_best_regressor.pkl",
        "qsar_best_classifier.pkl",
        "scaler_qsar.joblib",
        "qsar_feature_names.txt"
    ]
    
    for file_name in model_files:
        file_path = models_dir / file_name
        if file_path.exists():
            print(f"✅ {file_name} already exists")
        else:
            print(f"📥 Please place {file_name} in models/ folder")
    
    print("\n✅ Models check complete!")

if __name__ == "__main__":
    download_models() 