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

