"""
Configuration module
"""

import yaml
import os
from pathlib import Path

def load_config():
    """Load configuration from config.yaml"""
    config_path = Path(__file__).parent / "config.yaml"
    
    if not config_path.exists():
        return {
            'models': {
                'qsar_regressor': 'models/qsar_best_regressor.pkl',
                'qsar_classifier': 'models/qsar_best_classifier.pkl',
                'scalers': {
                    'qsar': 'models/scaler_qsar.joblib'
                },
                'feature_names': {
                    'qsar': 'models/qsar_feature_names.txt'
                }
            },
            'api': {
                'title': 'QSAR Prediction API',
                'version': '1.0.0'
            }
        }
    
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)  