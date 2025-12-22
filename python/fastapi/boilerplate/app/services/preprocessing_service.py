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

