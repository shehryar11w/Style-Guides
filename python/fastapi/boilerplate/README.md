# FastAPI AI Application Boilerplate

A complete FastAPI application boilerplate optimized for AI/ML model serving.

## Setup Instructions

### 1. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Variables

Create a `.env` file in the root directory:

```env
DEBUG=False
CORS_ORIGINS=["http://localhost:3000","http://localhost:8000"]
MODELS_DIR=./models
DEFAULT_MODEL_VERSION=latest
```

### 4. Create Models Directory

```bash
mkdir models
```

### 5. Run Development Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- API: `http://localhost:8000`
- Docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure

- `app/main.py`: Application entry point
- `app/api/`: API endpoints organized by version
- `app/models/`: AI/ML model wrappers
- `app/services/`: Business logic and services
- `app/core/`: Core configuration and exceptions
- `models/`: Trained model files (not in git)

## Available Endpoints

- `GET /`: Root endpoint
- `GET /health`: Health check
- `POST /api/v1/inference/predict`: Single prediction
- `POST /api/v1/inference/predict/batch`: Batch prediction

## Development

- Use async/await for I/O operations
- Follow type hints for all functions
- Use Pydantic models for validation
- Implement proper error handling
- Add tests for all endpoints

## Testing

```bash
pytest
```

## Production Deployment

1. Set `DEBUG=False` in `.env`
2. Use production ASGI server (Gunicorn with Uvicorn workers)
3. Configure proper CORS origins
4. Set up model versioning
5. Implement monitoring and logging

