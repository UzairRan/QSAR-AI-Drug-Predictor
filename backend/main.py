"""
QSAR Prediction API
FastAPI Backend for drug activity prediction
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from config.logging_config import logger
from backend.api.routes import router

# Create FastAPI app
app = FastAPI(
    title="QSAR Prediction API",
    description="Predict pIC50 and activity class from SMILES strings",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "QSAR Prediction API",
        "version": "1.0.0",
        "endpoints": {
            "/predict": "POST - Predict pIC50 and activity class",
            "/predict/batch": "POST - Batch prediction from CSV",
            "/explain": "POST - Get SHAP explanations",
            "/models": "GET - List available models",
            "/health": "GET - Health check"
        }
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "models_loaded": True,
        "api_version": "1.0.0"
    }

if __name__ == "__main__":
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 