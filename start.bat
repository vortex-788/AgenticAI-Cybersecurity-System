@echo off
REM ============================================
REM AgenticAI Cybersecurity System Startup
REM ============================================

cls
echo.
echo ============================================
echo   AgenticAI Cybersecurity System
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo ✓ Python is installed
echo.

REM Navigate to project directory
cd /d "%~dp0"

REM Initialize database if needed
echo ✓ Initializing database...
python init_db.py >nul 2>&1
if errorlevel 1 (
    echo WARNING: Could not initialize database
)

echo.
echo ============================================
echo   Starting Services
echo ============================================
echo.

REM Start Backend API Server
echo Starting Backend API Server (Port 8000)...
start "AgenticAI Backend" cmd /k "python run_server.py"

REM Wait for backend to start
timeout /t 3 /nobreak >nul

REM Start Frontend Server
echo Starting Frontend Server (Port 8080)...
start "AgenticAI Frontend" cmd /k "python frontend_server.py"

echo.
echo ============================================
echo   Services Started!
echo ============================================
echo.
echo ✓ Backend API: http://localhost:8000
echo ✓ Frontend:    http://localhost:8080
echo ✓ API Docs:    http://localhost:8000/docs
echo.
echo Open your browser and go to: http://localhost:8080
echo.
echo Press Ctrl+C in each window to stop services
echo ============================================
echo.

pause
