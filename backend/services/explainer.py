"""
SHAP Explanation Service
"""

import shap
import numpy as np
import joblib
from typing import Dict, Any
from rdkit import Chem
from rdkit.Chem import Descriptors
import traceback
import pandas as pd

from config.logging_config import logger

class ExplainerService:
    """Service for generating SHAP explanations"""
    
    def __init__(self):
        self.explainer = None
        self.feature_names = None
        self.scaler = None
        self._load_explainer()
    
    def _load_explainer(self):
        """Load SHAP explainer with correct data types"""
        try:
            logger.info("Starting SHAP explainer loading...")
            
            # Load feature names
            with open('models/qsar_feature_names.txt', 'r') as f:
                self.feature_names = [line.strip() for line in f.readlines()]
            logger.info(f"Loaded {len(self.feature_names)} feature names: {self.feature_names}")
            
            # Load model
            model = joblib.load('models/qsar_best_regressor.pkl')
            logger.info(f"Loaded regression model: {type(model)}")
            
            # Load scaler
            self.scaler = joblib.load('models/scaler_qsar.joblib')
            logger.info("Loaded scaler")
            
            # Create background data
            try:
                background_data = np.load('models/shap_background.npy')
                # Ensure correct dtype and shape
                background_data = np.array(background_data, dtype=np.float64)
                if len(background_data.shape) == 1:
                    background_data = background_data.reshape(1, -1)
                logger.info(f"Loaded SHAP background data: {background_data.shape}")
            except (FileNotFoundError, IOError) as e:
                logger.warning(f"Background file not found: {e}")
                background_data = np.random.randn(50, len(self.feature_names)).astype(np.float64)
                logger.info(f"Generated random background data: {background_data.shape}")
            
            # Verify background data has correct shape
            if background_data.shape[1] != len(self.feature_names):
                logger.warning(f"Background feature count mismatch: {background_data.shape[1]} vs {len(self.feature_names)}")
                background_data = np.random.randn(50, len(self.feature_names)).astype(np.float64)
                logger.info(f"Regenerated background data: {background_data.shape}")
            
            # Create explainer
            import time
            start_time = time.time()
            
            # Try different SHAP initialization methods
            try:
                # Method 1: TreeExplainer with background
                self.explainer = shap.TreeExplainer(model, background_data)
            except Exception as e1:
                logger.warning(f"TreeExplainer with background failed: {e1}")
                try:
                    # Method 2: TreeExplainer without background
                    self.explainer = shap.TreeExplainer(model)
                except Exception as e2:
                    logger.warning(f"TreeExplainer without background failed: {e2}")
                    # Method 3: Explainer
                    self.explainer = shap.Explainer(model)
            
            logger.info(f"SHAP explainer created in {time.time() - start_time:.2f}s")
            logger.info("SHAP explainer loaded successfully!")
            
        except Exception as e:
            logger.error(f"SHAP explainer loading failed: {str(e)}")
            logger.error(f"Full traceback: {traceback.format_exc()}")
            self.explainer = None
    
    def get_explanation(self, smiles: str) -> Dict[str, Any]:
        """Generate SHAP explanation for a SMILES"""
        if self.explainer is None:
            logger.warning(f"SHAP explainer not available for {smiles}")
            return {"error": "SHAP explainer not available"}
        
        try:
            # Validate SMILES
            mol = Chem.MolFromSmiles(smiles)
            if mol is None:
                raise ValueError(f"Invalid SMILES: {smiles}")
            
            # Calculate 8 descriptors (matching training)
            selected_descriptors = [
                'MolWt', 'NumHDonors', 'NumHAcceptors', 
                'TPSA', 'NumRotatableBonds',
                'RingCount', 'HeavyAtomCount', 'NumAromaticRings'
            ]
            
            features = []
            for desc_name in selected_descriptors:
                try:
                    func = getattr(Descriptors, desc_name)
                    value = func(mol)
                    features.append(float(value) if value is not None else 0.0)
                except Exception as e:
                    logger.warning(f"Failed to calculate {desc_name}: {e}")
                    features.append(0.0)
            
            # Convert to numpy array with correct dtype
            features = np.array(features, dtype=np.float64).reshape(1, -1)
            logger.info(f"Raw features: {features.shape}")
            
            # Scale features
            features_scaled = self.scaler.transform(features)
            logger.info(f"Scaled features: {features_scaled.shape}")
            
            # Get SHAP values
            shap_values = self.explainer.shap_values(features_scaled)
            
            # Handle different SHAP return types
            if isinstance(shap_values, list):
                shap_values = shap_values[0]  # For multi-output models
            
            # Format results
            feature_importance = []
            expected_value = self.explainer.expected_value
            if isinstance(expected_value, (list, np.ndarray)):
                expected_value = expected_value[0]
            
            for i, (name, value) in enumerate(zip(self.feature_names, features_scaled[0])):
                shap_val = shap_values[0][i] if len(shap_values.shape) > 1 else shap_values[i]
                feature_importance.append({
                    'feature': name,
                    'value': float(value),
                    'shap_value': float(shap_val)
                })
            
            feature_importance.sort(key=lambda x: abs(x['shap_value']), reverse=True)
            
            return {
                'smiles': smiles,
                'base_value': float(expected_value),
                'prediction': float(np.sum(shap_values) + expected_value),
                'feature_importance': feature_importance[:5]
            }
            
        except Exception as e:
            logger.error(f"SHAP explanation error: {str(e)}")
            logger.error(traceback.format_exc())
            return {"error": f"Failed to generate explanation: {str(e)}"}  