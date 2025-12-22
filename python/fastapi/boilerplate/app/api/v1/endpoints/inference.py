from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.api.v1.schemas import PredictionRequest, PredictionResponse, BatchPredictionRequest
from app.services.inference_service import InferenceService
from app.dependencies import get_inference_service

router = APIRouter()

@router.post("/predict", response_model=PredictionResponse)
async def predict(
    request: PredictionRequest,
    service: InferenceService = Depends(get_inference_service)
) -> PredictionResponse:
    """
    Predict the class of input text using the trained model.
    
    - **text**: Input text to classify
    - **model_version**: Version of the model to use (default: latest)
    """
    try:
        result = await service.predict(request.text, request.model_version)
        return PredictionResponse(**result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
        )

@router.post("/predict/batch", response_model=List[PredictionResponse])
async def predict_batch(
    request: BatchPredictionRequest,
    service: InferenceService = Depends(get_inference_service)
) -> List[PredictionResponse]:
    """Batch prediction endpoint for multiple inputs."""
    if len(request.texts) > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Batch size cannot exceed 100"
        )
    
    try:
        results = await service.predict_batch(request.texts, request.model_version)
        return [PredictionResponse(**r) for r in results]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Batch prediction failed: {str(e)}"
        )

