#!/usr/bin/env pwsh

# Healthcare AI Chatbot - Development Startup
Write-Host "🏥 Healthcare AI Chatbot - Development Mode" -ForegroundColor Green
Write-Host "===========================================" -ForegroundColor Blue

# Check if .env exists
if (!(Test-Path ".env")) {
    Write-Host "Creating .env file from template..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "⚠️ Please edit .env and add your OpenAI API key!" -ForegroundColor Red
    Write-Host "Then run this script again." -ForegroundColor Yellow
    exit 1
}

Write-Host "Starting backend and frontend servers..." -ForegroundColor Blue
Write-Host ""
Write-Host "Backend will be available at: http://localhost:8000" -ForegroundColor Cyan
Write-Host "Frontend will be available at: http://localhost:3000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop both servers" -ForegroundColor Yellow
Write-Host ""

# Start backend in background
Start-Job -ScriptBlock {
    Set-Location $using:PWD
    cd backend/app
    python main.py
} -Name "backend"

# Wait a moment for backend to start
Start-Sleep -Seconds 3

# Start frontend
cd frontend
npm start