"""
Feature Engineering Service
"""

import numpy as np
from rdkit import Chem
from rdkit.Chem import Descriptors
from typing import Dict, Any, List

from config.logging_config import logger

class FeatureEngineerService:
    """Service for calculating molecular features"""
    
    def __init__(self):
        self.selected_descriptors = [
            'MolWt', 'NumHDonors', 'NumHAcceptors', 
            'TPSA', 'NumRotatableBonds',
            'RingCount', 'HeavyAtomCount', 'NumAromaticRings'
        ]
    
    def calculate_rdkit_descriptors(self, smiles: str) -> np.ndarray:
        """
        Calculate RDKit descriptors for a single SMILES
        """
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            raise ValueError(f"Invalid SMILES: {smiles}")
        
        features = []
        for desc_name in self.selected_descriptors:
            try:
                func = getattr(Descriptors, desc_name)
                value = func(mol)
                features.append(float(value) if value is not None else 0.0)
            except:
                features.append(0.0)
        
        return np.array(features)
    
    def calculate_all_features(self, smiles: str) -> Dict[str, Any]:
        """
        Calculate all molecular features
        """
        try:
            descriptors = self.calculate_rdkit_descriptors(smiles)
            return {
                'descriptors': descriptors,
                'descriptor_names': self.selected_descriptors
            }
        except Exception as e:
            logger.error(f"Feature calculation error for {smiles}: {str(e)}")
            raise
    
    def batch_calculate_features(self, smiles_list: List[str]) -> List[Dict[str, Any]]:
        """
        Calculate features for multiple SMILES
        """
        results = []
        for smiles in smiles_list:
            try:
                features = self.calculate_all_features(smiles)
                results.append({'smiles': smiles, **features})
            except:
                results.append({
                    'smiles': smiles,
                    'descriptors': [np.nan] * len(self.selected_descriptors),
                    'error': 'Failed to calculate features'
                })
        return results  