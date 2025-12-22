# FastAPI Style Guide and Design Patterns (AI-Focused)

## Overview

FastAPI is a modern, fast web framework for building APIs with Python, based on standard Python type hints. This guide focuses on FastAPI patterns optimized for AI/ML applications, including model serving, inference endpoints, and AI service integration.

## Design Philosophy

- **High Performance**: Built on Starlette and Pydantic for speed
- **Type Safety**: Leverage Python type hints for validation
- **Async First**: Native async/await support for concurrent operations
- **AI/ML Ready**: Optimized for serving ML models and AI services
- **Auto Documentation**: Automatic OpenAPI/Swagger documentation
- **Dependency Injection**: Built-in DI system for clean architecture

## Directory Structure

```
fastapi-app/
├── app/
│   ├── __init__.py
│   ├── main.py                          # Application entry point
│   ├── config.py                        # Configuration settings
│   ├── dependencies.py                  # Shared dependencies
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── router.py                # Main router
│   │   │   ├── endpoints/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── health.py
│   │   │   │   ├── inference.py        # AI inference endpoints
│   │   │   │   ├── models.py           # Model management
│   │   │   │   └── predictions.py      # Prediction endpoints
│   │   │   └── schemas.py              # Pydantic models
│   ├── core/
│   │   ├── __init__.py
│   │   ├── security.py                 # Authentication/authorization
│   │   ├── exceptions.py               # Custom exceptions
│   │   └── config.py                   # Core configuration
│   ├── models/                         # AI/ML models
│   │   ├── __init__.py
│   │   ├── base.py                     # Base model interface
│   │   ├── text_classifier.py
│   │   ├── image_classifier.py
│   │   └── model_manager.py            # Model loading/caching
│   ├── services/                       # Business logic
│   │   ├── __init__.py
│   │   ├── inference_service.py        # Inference orchestration
│   │   ├── model_service.py            # Model management
│   │   └── preprocessing_service.py    # Data preprocessing
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── helpers.py
│   │   ├── validators.py
│   │   └── formatters.py
│   └── tests/
│       ├── __init__.py
│       ├── test_api/
│       ├── test_services/
│       └── conftest.py
├── models/                             # Trained model files
│   ├── text_classifier.pkl
│   └── image_classifier.h5
├── data/                               # Sample data
│   └── samples/
├── requirements.txt
├── requirements-dev.txt
├── .env
├── .gitignore
└── README.md
```

### Directory Structure Explanation

- **`app/api/`**: API endpoints organized by version
- **`app/models/`**: AI/ML model wrappers and interfaces
- **`app/services/`**: Business logic and service layer
- **`app/core/`**: Core functionality (security, config, exceptions)
- **`models/`**: Trained model files (not in git)
- **`data/`**: Sample data for testing

## Naming Conventions

### Files and Directories
- **Files**: snake_case (`inference_service.py`, `model_manager.py`)
- **Directories**: snake_case (`api/`, `services/`)
- **Classes**: PascalCase (`InferenceService`, `ModelManager`)
- **Functions**: snake_case (`predict_text`, `load_model`)
- **Variables**: snake_case (`model_instance`, `prediction_result`)
- **Constants**: UPPER_SNAKE_CASE (`MAX_BATCH_SIZE`, `MODEL_PATH`)

### API Endpoints
- **Routes**: Use kebab-case in URLs (`/api/v1/text-classification`)
- **Endpoint functions**: snake_case (`predict_text`, `classify_image`)

## Code Style Guidelines

### Python Style
- Follow **PEP 8** guidelines
- Use **4 spaces** for indentation
- Maximum line length: **88 characters** (Black formatter)
- Use **type hints** for all function signatures
- Use **async/await** for I/O operations

### FastAPI-Specific Style
- Use **Pydantic models** for request/response validation
- Use **dependency injection** for shared resources
- Use **async endpoints** for concurrent operations
- Document endpoints with **docstrings** and **response_model**

### Example Code Style

```python
# Good
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional
from app.services.inference_service import InferenceService
from app.dependencies import get_inference_service

router = APIRouter(prefix="/api/v1/inference", tags=["inference"])

class TextInput(BaseModel):
    text: str = Field(..., min_length=1, max_length=10000)
    model_version: Optional[str] = "latest"

class PredictionOutput(BaseModel):
    prediction: str
    confidence: float
    model_version: str

@router.post("/predict", response_model=PredictionOutput)
async def predict_text(
    input_data: TextInput,
    service: InferenceService = Depends(get_inference_service)
) -> PredictionOutput:
    """
    Predict the class of input text using the trained model.
    
    - **text**: Input text to classify
    - **model_version**: Version of the model to use (default: latest)
    """
    try:
        result = await service.predict(input_data.text, input_data.model_version)
        return PredictionOutput(
            prediction=result["label"],
            confidence=result["confidence"],
            model_version=result["model_version"]
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
        )

# Bad
from fastapi import APIRouter
# No type hints, no validation, no error handling
router = APIRouter()

@router.post("/predict")
def predict(text):  # No type hints, not async
    return {"result": "some prediction"}  # No validation, no error handling
```

## Component Patterns

### Main Application Pattern

```python
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_router
from app.core.config import settings

app = FastAPI(
    title="AI API",
    description="FastAPI application for AI/ML model serving",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "AI API is running", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

### Router Pattern

```python
# app/api/v1/router.py
from fastapi import APIRouter
from app.api.v1.endpoints import health, inference, models

api_router = APIRouter()

api_router.include_router(health.router, tags=["health"])
api_router.include_router(inference.router, prefix="/inference", tags=["inference"])
api_router.include_router(models.router, prefix="/models", tags=["models"])
```

### Endpoint Pattern (AI Inference)

```python
# app/api/v1/endpoints/inference.py
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from typing import List
from app.schemas.inference import PredictionRequest, PredictionResponse, BatchPredictionRequest
from app.services.inference_service import InferenceService
from app.dependencies import get_inference_service

router = APIRouter()

@router.post("/predict", response_model=PredictionResponse)
async def predict(
    request: PredictionRequest,
    service: InferenceService = Depends(get_inference_service)
) -> PredictionResponse:
    """Single prediction endpoint."""
    result = await service.predict(request.text, request.model_version)
    return PredictionResponse(**result)

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
    
    results = await service.predict_batch(request.texts, request.model_version)
    return [PredictionResponse(**r) for r in results]

@router.post("/predict/async")
async def predict_async(
    request: PredictionRequest,
    background_tasks: BackgroundTasks,
    service: InferenceService = Depends(get_inference_service)
):
    """Async prediction with background task."""
    task_id = await service.queue_prediction(request.text, request.model_version)
    background_tasks.add_task(service.process_queued_prediction, task_id)
    return {"task_id": task_id, "status": "queued"}
```

### Pydantic Schema Pattern

```python
# app/api/v1/schemas.py
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime

class PredictionRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=10000, description="Input text to classify")
    model_version: Optional[str] = Field("latest", description="Model version to use")
    
    @validator('text')
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
    texts: List[str] = Field(..., min_items=1, max_items=100)
    model_version: Optional[str] = "latest"
```

### Service Pattern (AI Model Service)

```python
# app/services/inference_service.py
from typing import Dict, List, Optional
import asyncio
from app.models.model_manager import ModelManager
from app.services.preprocessing_service import PreprocessingService
import time

class InferenceService:
    def __init__(
        self,
        model_manager: ModelManager,
        preprocessing_service: PreprocessingService
    ):
        self.model_manager = model_manager
        self.preprocessing_service = preprocessing_service
    
    async def predict(
        self,
        text: str,
        model_version: Optional[str] = "latest"
    ) -> Dict:
        """Perform single prediction."""
        start_time = time.time()
        
        # Preprocess input
        processed_text = await self.preprocessing_service.preprocess(text)
        
        # Load model
        model = await self.model_manager.get_model(model_version)
        
        # Run inference
        prediction = await model.predict(processed_text)
        
        processing_time = time.time() - start_time
        
        return {
            "label": prediction["label"],
            "confidence": prediction["confidence"],
            "model_version": model.version,
            "processing_time": processing_time
        }
    
    async def predict_batch(
        self,
        texts: List[str],
        model_version: Optional[str] = "latest"
    ) -> List[Dict]:
        """Perform batch predictions."""
        # Preprocess all texts
        processed_texts = await asyncio.gather(*[
            self.preprocessing_service.preprocess(text) for text in texts
        ])
        
        # Load model once
        model = await self.model_manager.get_model(model_version)
        
        # Run batch inference
        predictions = await model.predict_batch(processed_texts)
        
        return predictions
```

### Model Manager Pattern

```python
# app/models/model_manager.py
from typing import Dict, Optional
from pathlib import Path
import asyncio
from app.models.base import BaseModel

class ModelManager:
    def __init__(self, models_dir: Path):
        self.models_dir = models_dir
        self._models: Dict[str, BaseModel] = {}
        self._lock = asyncio.Lock()
    
    async def get_model(self, version: str = "latest") -> BaseModel:
        """Get model instance, loading if necessary."""
        async with self._lock:
            if version not in self._models:
                self._models[version] = await self._load_model(version)
            return self._models[version]
    
    async def _load_model(self, version: str) -> BaseModel:
        """Load model from disk."""
        model_path = self.models_dir / f"model_{version}.pkl"
        if not model_path.exists():
            raise FileNotFoundError(f"Model version {version} not found")
        
        # Load model (implementation depends on model type)
        model = BaseModel.load(str(model_path))
        model.version = version
        return model
    
    async def reload_model(self, version: str):
        """Reload a specific model."""
        async with self._lock:
            if version in self._models:
                del self._models[version]
            await self.get_model(version)
```

### Dependency Injection Pattern

```python
# app/dependencies.py
from functools import lru_cache
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
```

## AI/ML Specific Patterns

### Model Wrapper Pattern

```python
# app/models/base.py
from abc import ABC, abstractmethod
from typing import Dict, List, Any

class BaseModel(ABC):
    """Base class for AI/ML models."""
    
    def __init__(self, version: str):
        self.version = version
        self._model = None
    
    @abstractmethod
    async def load(self, path: str):
        """Load model from file."""
        pass
    
    @abstractmethod
    async def predict(self, input_data: Any) -> Dict:
        """Perform single prediction."""
        pass
    
    @abstractmethod
    async def predict_batch(self, input_data: List[Any]) -> List[Dict]:
        """Perform batch predictions."""
        pass

# app/models/text_classifier.py
import pickle
import numpy as np
from app.models.base import BaseModel

class TextClassifier(BaseModel):
    """Text classification model wrapper."""
    
    async def load(self, path: str):
        """Load scikit-learn model."""
        with open(path, 'rb') as f:
            self._model = pickle.load(f)
    
    async def predict(self, text: str) -> Dict:
        """Predict class for single text."""
        # Preprocess and predict
        prediction = self._model.predict([text])[0]
        probabilities = self._model.predict_proba([text])[0]
        confidence = float(np.max(probabilities))
        
        return {
            "label": str(prediction),
            "confidence": confidence
        }
    
    async def predict_batch(self, texts: List[str]) -> List[Dict]:
        """Predict classes for batch of texts."""
        predictions = self._model.predict(texts)
        probabilities = self._model.predict_proba(texts)
        
        results = []
        for pred, probs in zip(predictions, probabilities):
            results.append({
                "label": str(pred),
                "confidence": float(np.max(probs))
            })
        
        return results
```

### Preprocessing Service Pattern

```python
# app/services/preprocessing_service.py
import re
from typing import List
import asyncio

class PreprocessingService:
    """Service for text preprocessing."""
    
    async def preprocess(self, text: str) -> str:
        """Preprocess single text."""
        # Run preprocessing in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self._preprocess_sync,
            text
        )
    
    def _preprocess_sync(self, text: str) -> str:
        """Synchronous preprocessing."""
        # Remove special characters
        text = re.sub(r'[^\w\s]', '', text)
        # Lowercase
        text = text.lower()
        # Remove extra whitespace
        text = ' '.join(text.split())
        return text
    
    async def preprocess_batch(self, texts: List[str]) -> List[str]:
        """Preprocess batch of texts."""
        return await asyncio.gather(*[
            self.preprocess(text) for text in texts
        ])
```

## Error Handling Patterns

### Custom Exceptions

```python
# app/core/exceptions.py
from fastapi import HTTPException, status

class ModelNotFoundError(HTTPException):
    def __init__(self, version: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Model version {version} not found"
        )

class InferenceError(HTTPException):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Inference failed: {message}"
        )

class ValidationError(HTTPException):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=message
        )
```

### Exception Handler

```python
# app/main.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.core.exceptions import ModelNotFoundError, InferenceError

@app.exception_handler(ModelNotFoundError)
async def model_not_found_handler(request: Request, exc: ModelNotFoundError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )

@app.exception_handler(InferenceError)
async def inference_error_handler(request: Request, exc: InferenceError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )
```

## Testing Patterns

### API Testing

```python
# app/tests/test_api/test_inference.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_predict_endpoint():
    response = client.post(
        "/api/v1/inference/predict",
        json={"text": "This is a test", "model_version": "latest"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert "confidence" in data
    assert 0 <= data["confidence"] <= 1

def test_predict_batch():
    response = client.post(
        "/api/v1/inference/predict/batch",
        json={
            "texts": ["Text 1", "Text 2", "Text 3"],
            "model_version": "latest"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 3
```

## Best Practices

### Performance
- Use **async/await** for I/O operations
- Implement **model caching** to avoid reloading
- Use **batch processing** when possible
- Consider **model quantization** for faster inference
- Use **connection pooling** for database operations

### AI/ML Specific
- **Version models** for easy rollback
- **Monitor model performance** and drift
- **Cache predictions** for identical inputs
- **Validate inputs** before preprocessing
- **Log predictions** for analysis

### Security
- Validate and sanitize all inputs
- Rate limit inference endpoints
- Authenticate model management endpoints
- Use environment variables for secrets
- Implement request size limits

## Dependencies

### Core Dependencies
- **fastapi**: ^0.104.1
- **uvicorn[standard]**: ^0.24.0 (ASGI server)
- **pydantic**: ^2.5.0 (validation)
- **python-multipart**: ^0.0.6 (file uploads)

### AI/ML Dependencies
- **numpy**: ^1.24.3
- **scikit-learn**: ^1.3.2
- **tensorflow**: ^2.15.0 (optional)
- **torch**: ^2.1.0 (optional)
- **transformers**: ^4.35.0 (optional, for NLP)

### Development Dependencies
- **pytest**: ^7.4.3
- **pytest-asyncio**: ^0.21.1
- **httpx**: ^0.25.1 (for testing)
- **black**: ^23.11.0
- **flake8**: ^6.1.0

## Additional Resources

- [FastAPI Official Documentation](https://fastapi.tiangolo.com/)
- [FastAPI Best Practices](https://github.com/zhanymkanov/fastapi-best-practices)
- [MLOps with FastAPI](https://mlops.community/)

