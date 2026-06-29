"""
SHAP Explanation Service
"""

import shap
import numpy as np
import joblib
from typing import Dict, Any
from rdkit import Chem
from rdkit.Chem import Descriptors

from config.logging_config import logger

class ExplainerService:
    """Service for generating SHAP explanations"""
    
    def __init__(self):
        self.explainer = None
        self.feature_names = None
        self._load_explainer()
    
    def _load_explainer(self):
        """Load SHAP explainer"""
        try:
            with open('models/qsar_feature_names.txt', 'r') as f:
                self.feature_names = [line.strip() for line in f.readlines()]
            
            model = joblib.load('models/qsar_best_regressor.pkl')
            background_data = np.random.randn(100, len(self.feature_names))
            self.explainer = shap.TreeExplainer(model, background_data)
            
            logger.info("✅ SHAP explainer loaded successfully!")
            
        except Exception as e:
            logger.warning(f"SHAP explainer loading failed: {str(e)}")
            self.explainer = None
    
    def get_explanation(self, smiles: str) -> Dict[str, Any]:
        """
        Generate SHAP explanation for a SMILES
        """
        if self.explainer is None:
            return {"error": "SHAP explainer not available"}
        
        try:
            mol = Chem.MolFromSmiles(smiles)
            if mol is None:
                raise ValueError(f"Invalid SMILES: {smiles}")
            
            selected_descriptors = ['MolWt', 'NumHDonors', 'NumHAcceptors', 
                                   'TPSA', 'NumRotatableBonds',
                                   'RingCount', 'HeavyAtomCount', 'NumAromaticRings']
            
            features = []
            for desc_name in selected_descriptors:
                try:
                    func = getattr(Descriptors, desc_name)
                    value = func(mol)
                    features.append(value)
                except:
                    features.append(0)
            
            features = np.array(features).reshape(1, -1)
            shap_values = self.explainer.shap_values(features)
            
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