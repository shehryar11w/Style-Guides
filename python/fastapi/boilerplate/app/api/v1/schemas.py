from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime

class PredictionRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=10000, description="Input text to classify")
    model_version: Optional[str] = Field("latest", description="Model version to use")
    
    @field_validator('text')
    @classmethod
    def validate_text(cls, v):
        if not v.strip():
            raise ValueError('Text cannot be empty or whitespace only')
        return v.strip()

class PredictionResponse(BaseModel):
    prediction: str = Field(..., description="Predicted class label")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    model_version: str = Field(..., description="Model version used")
    processing_time: float = Field(..., description="Processing time in seconds")
    timestamp: datetime = Field(default_factory=datetime.now)

class BatchPredictionRequest(BaseModel):
    texts: List[str] = Field(..., min_length=1, max_items=100)
    model_version: Optional[str] = "latest"

