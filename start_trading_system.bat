@echo off
echo ========================================
echo 🚀 Starting Advanced Trading System
echo ========================================
echo.

echo 📦 Installing backend dependencies...
cd backend
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Backend dependencies installation failed!
    pause
    exit /b 1
)
echo ✅ Backend dependencies installed
echo.

echo 📦 Installing frontend dependencies...
cd ../frontend
npm install
if %errorlevel% neq 0 (
    echo ❌ Frontend dependencies installation failed!
    pause
    exit /b 1
)
echo ✅ Frontend dependencies installed
echo.

echo 🔧 Checking N8N installation...
n8n --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  N8N not found. Installing globally...
    npm install n8n -g
    if %errorlevel% neq 0 (
        echo ❌ N8N installation failed!
        pause
        exit /b 1
    )
)
echo ✅ N8N is ready
echo.

echo 🌟 Starting services...
echo.

echo 📊 Starting N8N API Server (Terminal 1)
start "N8N API Server" cmd /k "cd backend && python n8n_api.py"

timeout /t 3 /nobreak >nul

echo 🤖 Starting N8N Workflow Engine (Terminal 2)
start "N8N Engine" cmd /k "n8n start"

timeout /t 3 /nobreak >nul

echo 🎨 Starting Frontend Dashboard (Terminal 3)
start "Frontend Dashboard" cmd /k "cd frontend && npm run dev"

echo.
echo ========================================
echo 🎉 All services started successfully!
echo ========================================
echo.
echo 🌐 Access your services:
echo    • Frontend Dashboard: http://localhost:5173
echo    • N8N Workflow UI:    http://localhost:5678
echo    • N8N API Server:     http://localhost:5001
echo.
echo 📖 Setup Guide: backend/N8N_SETUP_README.md
echo.
echo Press any key to close this window...
pause >nul
