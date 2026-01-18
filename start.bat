@echo off
echo 🏥 Starting AI Doctor Application
echo ==================================

REM Check if backend virtual environment exists
if not exist "backend\venv" (
    echo ❌ Backend virtual environment not found!
    echo Please run: cd backend ^&^& python -m venv venv ^&^& venv\Scripts\activate ^&^& pip install -r requirements.txt
    exit /b 1
)

REM Check if frontend node_modules exists
if not exist "frontend\node_modules" (
    echo ❌ Frontend dependencies not installed!
    echo Please run: cd frontend ^&^& npm install
    exit /b 1
)

REM Check if .env exists
if not exist "backend\.env" (
    echo ⚠️  Warning: backend\.env not found
    echo Please copy .env.example to .env and add your OpenAI API key
    exit /b 1
)

echo ✅ Starting backend server...
cd backend
start cmd /k "venv\Scripts\activate && python main.py"

timeout /t 3 /nobreak > nul

echo ✅ Starting frontend server...
cd ..\frontend
start cmd /k "npm run dev"

echo.
echo 🎉 Application started successfully!
echo ==================================
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Press any key to exit...
pause > nul
