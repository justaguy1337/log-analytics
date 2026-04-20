@echo off
REM Log Analytics Platform - Startup Script (Windows)

echo Starting Distributed Log Analytics Platform...
echo.

REM Check if backend and frontend directories exist
if not exist "backend" (
    echo Error: Backend directory not found
    exit /b 1
)
if not exist "frontend" (
    echo Error: Frontend directory not found
    exit /b 1
)

REM Start backend in new window
echo Starting Backend Server...
start "Log Analytics - Backend" cmd /k "cd backend && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"
timeout /t 2 /nobreak

REM Start frontend in new window
echo Starting Frontend Server...
start "Log Analytics - Frontend" cmd /k "cd frontend && npm run dev"
timeout /t 2 /nobreak

echo.
echo Platform is running!
echo.
echo Dashboard: http://localhost:5173
echo API: http://localhost:8000/api/v1
echo API Docs: http://localhost:8000/docs
echo.
echo Close the terminal windows to stop the servers
pause
