# AgenticAI Cybersecurity System Startup Script

Write-Host ""
Write-Host "============================================"
Write-Host "  AgenticAI Cybersecurity System" -ForegroundColor Cyan
Write-Host "============================================"
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Set working directory
$workingDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $workingDir

Write-Host "✓ Working directory: $workingDir" -ForegroundColor Green
Write-Host ""

# Initialize database
Write-Host "✓ Initializing database..." -ForegroundColor Yellow
python init_db.py 2>&1 | Out-Null

Write-Host ""
Write-Host "============================================"
Write-Host "  Starting Services" -ForegroundColor Cyan
Write-Host "============================================"
Write-Host ""

# Start Backend Server in new window
Write-Host "Starting Backend API Server (Port 8000)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$workingDir'; python run_server.py" -WindowStyle Normal

# Wait for backend to start
Start-Sleep -Seconds 3

# Start Frontend Server in new window
Write-Host "Starting Frontend Server (Port 8080)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$workingDir'; python frontend_server.py" -WindowStyle Normal

Write-Host ""
Write-Host "============================================"
Write-Host "  Services Started!" -ForegroundColor Green
Write-Host "============================================"
Write-Host ""
Write-Host "✓ Backend API: http://localhost:8000" -ForegroundColor Green
Write-Host "✓ Frontend:    http://localhost:8080" -ForegroundColor Green
Write-Host "✓ API Docs:    http://localhost:8000/docs" -ForegroundColor Green
Write-Host ""
Write-Host "Open your browser and go to: http://localhost:8080" -ForegroundColor Cyan
Write-Host ""
Write-Host "To stop the services, close the respective windows" -ForegroundColor Yellow
Write-Host "============================================"
Write-Host ""

# Keep this window open
Read-Host "Press Enter to exit this window"



#1 cd "c:\Users\Raghav\Downloads\AgenticAI-Cybersecurity-System\AgenticAI-Cybersecurity-System"
#2 python init_db.py
#3 python run_server.py
#4 python frontend_server.py