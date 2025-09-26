# AgenticMarketers Backend

FastAPI backend for the AgenticMarketers application.

## Setup

1. Install dependencies:
```bash
uv sync
```

2. Set up environment variables:
```bash
# Create .env file in project root
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
```

3. Run the backend:
```bash
python run_backend.py
```

## API Endpoints

- `GET /` - Health check
- `GET /health` - Detailed health check
- `POST /start_workflow` - Main workflow endpoint

## API Documentation

Once running, visit:
- http://localhost:8000/docs - Interactive API documentation
- http://localhost:8000/redoc - Alternative documentation format

## Testing

Test the workflow endpoint:
```bash
curl -X POST "http://localhost:8000/start_workflow" \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "Test Product",
    "product_description": "A great test product"
  }'
```
