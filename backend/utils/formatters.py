"""
Response Formatters
"""

from typing import Dict, Any, List
import pandas as pd
import json

class ResponseFormatter: 
    """Format responses for different outputs"""
    
    @staticmethod
    def format_prediction_for_display(prediction: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format prediction for display in frontend
        """
        return {
            'QSAR': {
                'pIC50': prediction['qsar']['pIC50'],
                'Activity': prediction['qsar']['activity_class'],
                'Confidence': f"{prediction['qsar']['confidence']*100:.1f}%"
            },
            'ADMET': {
                'BBB Penetration': '✓' if prediction['admet']['bbb_penetration']['value'] else '✗',
                'BBB Probability': f"{prediction['admet']['bbb_penetration']['probability']*100:.1f}%",
                'Pgp Substrate': '✓' if prediction['admet']['pgp_substrate']['value'] else '✗',
                'Pgp Probability': f"{prediction['admet']['pgp_substrate']['probability']*100:.1f}%",
                'CYP3A4 Inhibitor': '✓' if prediction['admet']['cyp3a4_inhibitor']['value'] else '✗',
                'CYP3A4 Probability': f"{prediction['admet']['cyp3a4_inhibitor']['probability']*100:.1f}%"
            }
        }
    
    @staticmethod
    def format_batch_for_download(results: List[Dict[str, Any]]) -> pd.DataFrame:
        """
        Format batch results for CSV download
        """
        data = []
        for result in results:
            data.append({
                'SMILES': result['smiles'],
                'pIC50': result['qsar']['pIC50'],
                'Activity_Class': result['qsar']['activity_class'],
                'BBB_Penetration': result['admet']['bbb_penetration']['value'],
                'BBB_Probability': result['admet']['bbb_penetration']['probability'],
                'Pgp_Substrate': result['admet']['pgp_substrate']['value'],
                'Pgp_Probability': result['admet']['pgp_substrate']['probability'],
                'CYP3A4_Inhibitor': result['admet']['cyp3a4_inhibitor']['value'],
                'CYP3A4_Probability': result['admet']['cyp3a4_inhibitor']['probability']
            })
        return pd.DataFrame(data) 