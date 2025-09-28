# Healthcare Chatbot Backend Startup Script (PowerShell)
Write-Host "🏥 Starting Healthcare Chatbot Backend..." -ForegroundColor Green

# Check if virtual environment exists
if (!(Test-Path "venv")) {
    Write-Host "📦 Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate virtual environment
Write-Host "🔄 Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Install dependencies
Write-Host "📥 Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Check for environment file
if (!(Test-Path "../.env")) {
    Write-Host "⚠️  No .env file found. Please copy .env.example to .env and add your OpenAI API key." -ForegroundColor Red
    exit 1
}

# Start the server
Write-Host "🚀 Starting FastAPI server..." -ForegroundColor Green
Set-Location app
python main.py