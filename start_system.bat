@echo off
echo ============================================
echo  Starting AgenticAI Cybersecurity System
echo ============================================

REM Activate virtual environment if present
if exist venv (
    call venv\Scripts\activate
)

REM Start FastAPI backend in a new window
start "AgenticAI Backend" cmd /k "python -m app.main"

REM Wait a bit to let backend start
timeout /t 5 /nobreak >nul

REM Start mock alert generator
start "Mock Generator" cmd /k "python mock_generator.py"

echo --------------------------------------------
echo Both backend and mock generator are running.
echo Visit http://127.0.0.1:8000/docs to test API.
echo --------------------------------------------
pause
