"""
API Routes for QSAR Predictions
"""

from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from typing import List, Dict, Any
import pandas as pd
import io

from backend.api.models import (
    PredictionRequest, BatchPredictionRequest, ExplanationRequest,
    PredictionResponse, BatchPredictionResponse, ModelInfo
)
from backend.services.predictor import PredictorService
from backend.services.explainer import ExplainerService
from config.logging_config import logger

router = APIRouter(prefix="/api/v1", tags=["predictions"])

# Initialize services
predictor_service = PredictorService()
explainer_service = ExplainerService()

@router.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """
    Predict QSAR properties from a SMILES string
    """
    try:
        logger.info(f"Processing prediction for SMILES: {request.smiles[:50]}...")
        
        result = predictor_service.predict(request.smiles)
        
        if request.include_explanation:
            result['explanation'] = explainer_service.get_explanation(request.smiles)
        
        return PredictionResponse(**result)
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/predict/batch", response_model=BatchPredictionResponse)
async def predict_batch(request: BatchPredictionRequest):
    """
    Predict for multiple SMILES strings
    """
    try:
        logger.info(f"Processing batch prediction for {len(request.smiles_list)} molecules")
        
        results = []
        errors = []
        successful = 0
        
        for i, smiles in enumerate(request.smiles_list):
            try:
                result = predictor_service.predict(smiles)
                if request.include_explanation:
                    result['explanation'] = explainer_service.get_explanation(smiles)
                results.append(PredictionResponse(**result))
                successful += 1
            except Exception as e:
                errors.append({
                    "index": i,
                    "smiles": smiles,
                    "error": str(e)
                })
        
        return BatchPredictionResponse(
            results=results,
            total=len(request.smiles_list),
            successful=successful,
            failed=len(errors),
            errors=errors
        )
        
    except Exception as e:
        logger.error(f"Batch prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/predict/upload")
async def predict_upload(file: UploadFile = File(...)):
    """
    Upload CSV file for batch prediction
    """
    try:
        content = await file.read()
        df = pd.read_csv(io.StringIO(content.decode('utf-8')))
        
        if 'smiles' not in df.columns:
            raise HTTPException(
                status_code=400,
                detail="CSV must contain 'smiles' column"
            )
        
        smiles_list = df['smiles'].dropna().tolist()
        
        if len(smiles_list) > 100:
            raise HTTPException(
                status_code=400,
                detail="Maximum 100 molecules per batch"
            )
        
        results = []
        errors = []
        successful = 0
        
        for i, smiles in enumerate(smiles_list):
            try:
                result = predictor_service.predict(smiles)
                results.append({
                    'index': i,
                    'smiles': smiles,
                    'pIC50': result['qsar']['pIC50'],
                    'activity_class': result['qsar']['activity_class'],
                    'confidence': result['qsar']['confidence']
                })
                successful += 1
            except Exception as e:
                errors.append({
                    "index": i,
                    "smiles": smiles,
                    "error": str(e)
                })
        
        return JSONResponse({
            "results": results,
            "total": len(smiles_list),
            "successful": successful,
            "failed": len(errors),
            "errors": errors
        })
        
    except Exception as e:
        logger.error(f"Upload prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/explain")
async def explain(request: ExplanationRequest):
    """
    Get SHAP explanation for a SMILES
    """
    try:
        logger.info(f"Getting explanation for SMILES: {request.smiles[:50]}...")
        explanation = explainer_service.get_explanation(request.smiles)
        return JSONResponse(explanation)
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Explanation error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/models", response_model=List[ModelInfo])
async def get_models():
    """
    Get information about available models
    """
    try:
        models = predictor_service.get_model_info()
        return models
    except Exception as e:
        logger.error(f"Model info error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))  