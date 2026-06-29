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
        self._load_explainer()
    
    def _load_explainer(self):
        """Load SHAP explainer with fallback for deployment"""
        try:
            logger.info("Starting SHAP explainer loading...")
            
            # Load feature names
            with open('models/qsar_feature_names.txt', 'r') as f:
                self.feature_names = [line.strip() for line in f.readlines()]
            logger.info(f"Loaded {len(self.feature_names)} feature names")
            
            # Load model
            model = joblib.load('models/qsar_best_regressor.pkl')
            logger.info("Loaded regression model")
            
            # Create background data
            try:
                background_data = np.load('models/shap_background.npy')
                logger.info("Loaded SHAP background data from file")
            except (FileNotFoundError, IOError):
                logger.info("Generating random background data...")
                background_data = np.random.randn(50, len(self.feature_names))
                logger.info("Generated random SHAP background data")
            
            # Create explainer with timeout protection
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
        """
        Generate SHAP explanation for a SMILES
        """
        if self.explainer is None:
            logger.warning(f"SHAP explainer not available for {smiles}")
            return {"error": "SHAP explainer not available"}
        
        try:
            # Validate SMILES
            mol = Chem.MolFromSmiles(smiles)
            if mol is None:
                raise ValueError(f"Invalid SMILES: {smiles}")
            
            # Calculate descriptors
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
            
            features = np.array(features).reshape(1, -1)
            
            # Get SHAP values
            shap_values = self.explainer.shap_values(features)
            
            # Format results
            feature_importance = []
            for i, (name, value) in enumerate(zip(self.feature_names, features[0])):
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
            return {"error": f"Failed to generate explanation: {str(e)}"}  