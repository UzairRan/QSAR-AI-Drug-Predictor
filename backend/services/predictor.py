"""
Prediction Service - Core prediction logic
"""

import joblib
import numpy as np
from typing import Dict, Any, List
from rdkit import Chem
from rdkit.Chem import Descriptors

from config.logging_config import logger
from config import load_config

class PredictorService:
    """Service for making predictions using trained QSAR models"""
    
    def __init__(self):
        self.config = load_config()
        self.models = {}
        self.scalers = {}
        self.feature_names = {}
        self._load_models()
        
    def _load_models(self):
        """Load all trained models and scalers"""
        try:
            logger.info("Loading QSAR models...")
            
            self.models['qsar_regressor'] = joblib.load(
                self.config['models']['qsar_regressor']
            )
            self.models['qsar_classifier'] = joblib.load(
                self.config['models']['qsar_classifier']
            )
            
            logger.info("Loading scaler...")
            self.scalers['qsar'] = joblib.load(
                self.config['models']['scalers']['qsar']
            )
            
            logger.info("Loading feature names...")
            with open(self.config['models']['feature_names']['qsar'], 'r') as f:
                self.feature_names['qsar'] = [line.strip() for line in f.readlines()]
            
            logger.info("✅ All models loaded successfully!")
            
        except Exception as e:
            logger.error(f"Error loading models: {str(e)}")
            raise
    
    def _validate_smiles(self, smiles: str) -> bool:
        """Validate SMILES string using RDKit"""
        try:
            mol = Chem.MolFromSmiles(smiles)
            return mol is not None
        except:
            return False
    
    def _calculate_rdkit_features(self, smiles: str) -> np.ndarray:
        """Calculate RDKit descriptors for a SMILES"""
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            raise ValueError(f"Invalid SMILES: {smiles}")
        
        # 8 features - matching training
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
                features.append(np.nan)
        
        return np.array(features).reshape(1, -1)
    
    def _get_activity_class(self, pic50: float) -> str:
        """Convert pIC50 to activity class"""
        if pic50 >= 7.0:
            return 'Active'
        elif pic50 >= 5.0:
            return 'Moderate'
        else:
            return 'Inactive'
    
    def _get_confidence(self, prediction: float) -> float:
        """Calculate confidence score for prediction"""
        return min(0.95, max(0.5, 1 - abs(prediction - 6.5) / 10))
    
    def predict(self, smiles: str) -> Dict[str, Any]:
        """
        Make full prediction for a SMILES
        """
        if not self._validate_smiles(smiles):
            raise ValueError(f"Invalid SMILES string: {smiles}")
        
        try:
            # 1. Calculate RDKit features
            features = self._calculate_rdkit_features(smiles)
            
            # 2. Scale features
            scaled = self.scalers['qsar'].transform(features)
            
            # 3. QSAR Predictions
            pic50 = self.models['qsar_regressor'].predict(scaled)[0]
            activity_class = self._get_activity_class(pic50)
            confidence = self._get_confidence(pic50)
            
            return {
                'smiles': smiles,
                'qsar': {
                    'pIC50': round(float(pic50), 3),
                    'activity_class': activity_class,
                    'confidence': round(float(confidence), 3)
                }
            }
            
        except Exception as e:
            logger.error(f"Prediction error for {smiles}: {str(e)}")
            raise
    
    def get_model_info(self) -> List[Dict[str, Any]]:
        """Get information about loaded models"""
        return [
            {
                'name': 'QSAR Regressor',
                'type': 'Regression',
                'metrics': {'R²': 0.298, 'RMSE': 0.985},
                'features': self.feature_names['qsar'],
                'description': 'Predicts pIC50 values for COX-2 inhibition'
            },
            {
                'name': 'QSAR Classifier',
                'type': 'Classification',
                'metrics': {'AUC': 0.771, 'Accuracy': 0.758},
                'features': self.feature_names['qsar'],
                'description': 'Classifies molecules as Active/Inactive'
            }
        ]  