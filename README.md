# AgenticMarketers

AI-powered marketing content generation platform with WriterAgent integration.

## Quick Start

### Prerequisites
- Python 3.12+
- Node.js 18+
- OpenAI API key

### Setup

1. **Install Dependencies**
```bash
# Install Python dependencies
uv sync

# Install frontend dependencies
cd frontend
npm install
cd ..
```

2. **Environment Setup**
```bash
# Create .env file with your OpenAI API key
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
```

### Running the Application

#### Option 1: Start Everything at Once
```bash
./start_all.sh
```

#### Option 2: Start Services Separately

**Terminal 1 - Backend:**
```bash
uv run python start_backend.py
```

**Terminal 2 - Frontend:**
```bash
./start_frontend.sh
```

### Access Points

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## Testing the Application

1. **Fill out the form** with product information
2. **Click "Generate Content"** to create AI-powered captions
3. **Copy the caption** and use with your product images
4. **Post to social media** manually

## Features

- ✅ **AI-Generated Captions**: Uses WriterAgent for intelligent content
- ✅ **Product Information Form**: Comprehensive product details input
- ✅ **Mock Image Display**: Visual preview of content
- ✅ **Copy to Clipboard**: Easy content copying
- ✅ **Responsive Design**: Works on desktop and mobile
- ✅ **FastAPI Backend**: RESTful API with automatic documentation

## Project Structure

```
marketing-agent/
├── agents/
│   └── writer/
│       └── writer.py          # WriterAgent implementation
├── backend/
│   └── main.py                # FastAPI backend
├── frontend/
│   ├── pages/
│   │   └── index.tsx          # Main React page
│   └── styles/
│       └── globals.css         # Styling
├── prompts/
│   └── InputPrompt.py         # Data models
├── start_backend.py           # Backend startup script
├── start_frontend.sh          # Frontend startup script
└── start_all.sh               # Start everything script
```

## Development

### Backend Development
- FastAPI with automatic API documentation
- WriterAgent integration for AI content generation
- CORS enabled for frontend communication

### Frontend Development
- Next.js with TypeScript
- Black and white minimalist design
- Responsive form with advanced options
- Real-time content generation

## API Endpoints

- `GET /` - Health check
- `GET /health` - Detailed health status
- `POST /start_workflow` - Generate content from form data

## Troubleshooting

### Backend Issues
- Check OpenAI API key is set in `.env`
- Ensure port 8000 is available
- Check Python dependencies with `uv sync`

### Frontend Issues
- Ensure Node.js is installed
- Run `npm install` in frontend directory
- Check port 3000 is available

### Connection Issues
- Verify backend is running on http://localhost:8000
- Check CORS settings in backend
- Ensure both services are running simultaneously