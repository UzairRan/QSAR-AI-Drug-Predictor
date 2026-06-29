"""
MLflow Tracking Service
"""

import mlflow
import mlflow.sklearn
import mlflow.xgboost
from mlflow.tracking import MlflowClient
from typing import Dict, Any, Optional
import joblib
import os
from datetime import datetime

from config.logging_config import logger

class MLflowTracker:
    """Service for MLflow experiment tracking"""
    
    def __init__(self, tracking_uri: str = "mlflow/mlruns"):
        self.tracking_uri = tracking_uri
        self.experiment_name = "QSAR_ADMET_Platform"
        self.client = None
        
        self._setup_mlflow()
    
    def _setup_mlflow(self):
        """Setup MLflow tracking"""
        try:
            # Set tracking URI
            mlflow.set_tracking_uri(self.tracking_uri)
            
            # Create experiment if it doesn't exist
            try:
                self.experiment_id = mlflow.create_experiment(self.experiment_name)
            except:
                # Experiment already exists
                experiment = mlflow.get_experiment_by_name(self.experiment_name)
                self.experiment_id = experiment.experiment_id
            
            self.client = MlflowClient()
            
            logger.info(f"✅ MLflow tracking initialized at {self.tracking_uri}")
            
        except Exception as e:
            logger.warning(f"MLflow setup failed: {str(e)}")
            self.client = None
    
    def log_model(self, model_path: str, model_name: str, metrics: Dict[str, float], 
                  parameters: Optional[Dict[str, Any]] = None) -> str:
        """
        Log a model to MLflow
        """
        if self.client is None:
            logger.warning("MLflow client not available, skipping logging")
            return "MLflow not available"
        
        try:
            with mlflow.start_run(experiment_id=self.experiment_id, run_name=f"{model_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"):
                # Log parameters
                if parameters:
                    mlflow.log_params(parameters)
                
                # Log metrics
                if metrics:
                    mlflow.log_metrics(metrics)
                
                # Log model
                mlflow.sklearn.log_model(
                    sk_model=joblib.load(model_path),
                    artifact_path=f"models/{model_name}",
                    registered_model_name=model_name
                )
                
                # Get run ID
                run_id = mlflow.active_run().info.run_id
                
                logger.info(f"✅ Logged model {model_name} to MLflow (run_id: {run_id})")
                return run_id
                
        except Exception as e:
            logger.error(f"MLflow logging failed for {model_name}: {str(e)}")
            return f"Failed: {str(e)}"
    
    def log_all_models(self, model_paths: Dict[str, str], metrics: Dict[str, Dict[str, float]]):
        """
        Log all models to MLflow
        """
        results = {}
        for model_name, path in model_paths.items():
            model_metrics = metrics.get(model_name, {})
            run_id = self.log_model(path, model_name, model_metrics)
            results[model_name] = run_id
        
        return results
    
    def get_model_versions(self, model_name: str) -> list:
        """
        Get all versions of a model
        """
        if self.client is None:
            return []
        
        try:
            versions = self.client.search_model_versions(f"name='{model_name}'")
            return [{
                'version': v.version,
                'run_id': v.run_id,
                'stage': v.current_stage,
                'created_at': v.creation_timestamp
            } for v in versions]
        except Exception as e:
            logger.error(f"Failed to get model versions for {model_name}: {str(e)}")
            return []
    
    def promote_model(self, model_name: str, version: str, stage: str = "Production"):
        """
        Promote a model to a specific stage
        """
        if self.client is None:
            return "MLflow not available"
        
        try:
            self.client.transition_model_version_stage(
                name=model_name,
                version=version,
                stage=stage
            )
            logger.info(f"✅ Model {model_name} version {version} promoted to {stage}")
            return f"Successfully promoted to {stage}"
        except Exception as e:
            logger.error(f"Failed to promote model: {str(e)}")
            return f"Failed: {str(e)}"  