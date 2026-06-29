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
            logger.info(f"Loaded {len(self.feature_names)} feature names")
            
            # Load model
            model = joblib.load('models/qsar_best_regressor.pkl')
            logger.info("Loaded regression model")
            
            # Load scaler
            self.scaler = joblib.load('models/scaler_qsar.joblib')
            logger.info("Loaded scaler")
            
            # Create background data with CORRECT data type
            try:
                background_data = np.load('models/shap_background.npy')
                # Ensure float64 type
                background_data = background_data.astype(np.float64)
                logger.info(f"Loaded SHAP background data: {background_data.shape}")
            except (FileNotFoundError, IOError):
                logger.info("Generating random background data...")
                background_data = np.random.randn(50, len(self.feature_names)).astype(np.float64)
                logger.info(f"Generated random background data: {background_data.shape}")
            
            # Create explainer
            import time
            start_time = time.time()
            self.explainer = shap.TreeExplainer(model, background_data)
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
                except:
                    features.append(0.0)
            
            # Convert to numpy array with correct dtype
            features = np.array(features, dtype=np.float64).reshape(1, -1)
            
            # Scale features
            features_scaled = self.scaler.transform(features)
            
            # Get SHAP values
            shap_values = self.explainer.shap_values(features_scaled)
            
            # Format results
            feature_importance = []
            for i, (name, value) in enumerate(zip(self.feature_names, features_scaled[0])):
                feature_importance.append({
                    'feature': name,
                    'value': float(value),
                    'shap_value': float(shap_values[0][i])
                })
            
            feature_importance.sort(key=lambda x: abs(x['shap_value']), reverse=True)
            
            return {
                'smiles': smiles,
                'base_value': float(self.explainer.expected_value),
                'prediction': float(np.sum(shap_values) + self.explainer.expected_value),
                'feature_importance': feature_importance[:5]
            }
            
        except Exception as e:
            logger.error(f"SHAP explanation error: {str(e)}")
            logger.error(traceback.format_exc())
            return {"error": f"Failed to generate explanation: {str(e)}"}  