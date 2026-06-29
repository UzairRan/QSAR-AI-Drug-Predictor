"""
SMILES Validation Utilities
"""

from rdkit import Chem
from typing import Tuple, Optional, List

class SMILESValidator:
    """Validator for SMILES strings"""
    
    @staticmethod
    def validate_smiles(smiles: str) -> Tuple[bool, Optional[str]]:
        """
        Validate a SMILES string
        
        Returns:
            (is_valid, error_message)
        """
        if not smiles or not isinstance(smiles, str):
            return False, "SMILES must be a non-empty string"
        
        smiles = smiles.strip()
        if not smiles:
            return False, "SMILES cannot be empty"
        
        try:
            mol = Chem.MolFromSmiles(smiles)
            if mol is None:
                return False, "Invalid SMILES string"
            
            # Additional validation
            if mol.GetNumAtoms() == 0:
                return False, "SMILES contains no atoms"
            
            if mol.GetNumAtoms() > 200:
                return False, "Molecule too large (max 200 atoms)"
            
            return True, None
            
        except Exception as e:
            return False, f"SMILES parsing error: {str(e)}"
    
    @staticmethod
    def validate_batch(smiles_list: List[str]) -> List[Tuple[str, bool, Optional[str]]]:
        """
        Validate multiple SMILES
        """
        results = []
        for smiles in smiles_list:
            is_valid, error = SMILESValidator.validate_smiles(smiles)
            results.append((smiles, is_valid, error))
        return results 