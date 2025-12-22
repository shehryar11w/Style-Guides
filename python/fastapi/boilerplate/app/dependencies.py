from functools import lru_cache
from fastapi import Depends
from app.models.model_manager import ModelManager
from app.services.inference_service import InferenceService
from app.services.preprocessing_service import PreprocessingService
from app.core.config import settings
from pathlib import Path

@lru_cache()
def get_model_manager() -> ModelManager:
    """Get singleton model manager instance."""
    return ModelManager(models_dir=Path(settings.MODELS_DIR))

def get_preprocessing_service() -> PreprocessingService:
    """Get preprocessing service instance."""
    return PreprocessingService()

def get_inference_service(
    model_manager: ModelManager = Depends(get_model_manager),
    preprocessing_service: PreprocessingService = Depends(get_preprocessing_service)
) -> InferenceService:
    """Get inference service with dependencies."""
    return InferenceService(
        model_manager=model_manager,
        preprocessing_service=preprocessing_service
    )

