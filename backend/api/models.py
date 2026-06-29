"""
Pydantic models for API requests and responses
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime

# Request Models
class PredictionRequest(BaseModel):
    """Request model for single molecule prediction"""
    
    smiles: str = Field(..., description="SMILES string of the molecule")
    include_explanation: bool = Field(False, description="Include SHAP explanation")
    
    @validator('smiles')
    def validate_smiles(cls, v):
        if not v or not isinstance(v, str):
            raise ValueError("SMILES must be a non-empty string")
        return v.strip()
    
    class Config:
        json_schema_extra = {
            "example": {
                "smiles": "CC(=O)Oc1ccccc1C(=O)O",
                "include_explanation": True
            }
        }

class BatchPredictionRequest(BaseModel):
    """Request model for batch prediction"""
    
    smiles_list: List[str] = Field(..., description="List of SMILES strings")
    include_explanation: bool = Field(False, description="Include SHAP explanations")
    
    @validator('smiles_list')
    def validate_list(cls, v):
        if not v:
            raise ValueError("SMILES list cannot be empty")
        if len(v) > 100:
            raise ValueError("Maximum 100 molecules per batch")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "smiles_list": [
                    "CC(=O)Oc1ccccc1C(=O)O",
                    "CCOc1ccc(cc1)C(=O)O"
                ],
                "include_explanation": False
            }
        }

class ExplanationRequest(BaseModel):
    """Request model for SHAP explanation"""
    
    smiles: str = Field(..., description="SMILES string to explain")
    
    class Config:
        json_schema_extra = {
            "example": {
                "smiles": "CC(=O)Oc1ccccc1C(=O)O"
            }
        }

# Response Models
class QSARPrediction(BaseModel):
    """QSAR prediction results"""
    
    pIC50: float = Field(..., description="Predicted pIC50 value")
    activity_class: str = Field(..., description="Activity class: Active/Moderate/Inactive")
    confidence: float = Field(..., description="Prediction confidence (0-1)")

class PredictionResponse(BaseModel):
    """Complete prediction response"""
    
    smiles: str = Field(..., description="Input SMILES")
    molecule_id: Optional[str] = Field(None, description="Molecule identifier if provided")
    qsar: QSARPrediction = Field(..., description="QSAR predictions")
    explanation: Optional[Dict[str, Any]] = Field(None, description="SHAP explanation")
    timestamp: datetime = Field(default_factory=datetime.now, description="Prediction timestamp")

class BatchPredictionResponse(BaseModel):
    """Batch prediction response"""
    
    results: List[PredictionResponse] = Field(..., description="List of predictions")
    total: int = Field(..., description="Total molecules processed")
    successful: int = Field(..., description="Successfully predicted")
    failed: int = Field(..., description="Failed predictions")
    errors: List[Dict[str, str]] = Field([], description="Error messages for failed predictions")

class ModelInfo(BaseModel):
    """Model information response"""
    
    name: str
    type: str
    metrics: Dict[str, float]
    features: List[str]
    description: str

class HealthResponse(BaseModel):
    """Health check response"""
    
    status: str
    models_loaded: bool
    api_version: str   