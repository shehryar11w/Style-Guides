from typing import Dict, List, Optional
import asyncio
import time
from app.models.model_manager import ModelManager
from app.services.preprocessing_service import PreprocessingService

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
            "prediction": prediction["label"],
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

