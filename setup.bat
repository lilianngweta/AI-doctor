@echo off
REM AI Doctor - Quick Setup Script for Windows

echo ╔════════════════════════════════════════════════════════════╗
echo ║        🏥 AI Doctor - Quick Setup Assistant              ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Check Python
echo 🔍 Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)
for /f "tokens=2" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✅ Python %PYTHON_VERSION% found
echo.

REM Check Node
echo 🔍 Checking Node.js installation...
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed. Please install Node.js 16 or higher.
    pause
    exit /b 1
)
for /f %%i in ('node --version') do set NODE_VERSION=%%i
echo ✅ Node.js %NODE_VERSION% found
echo.

REM Backend setup
echo 📦 Setting up backend...
cd backend

if not exist "venv" (
    echo   → Creating virtual environment...
    python -m venv venv
)

echo   → Activating virtual environment...
call venv\Scripts\activate

echo   → Installing Python dependencies...
python -m pip install -q --upgrade pip
pip install -q -r requirements.txt

if not exist ".env" (
    echo   → Creating .env file...
    copy .env.example .env >nul
    echo.
    echo ⚠️  IMPORTANT: Please add your OpenAI API key to backend\.env
    echo    Edit the file and replace 'your_openai_api_key_here' with your actual key
    echo    Get your key from: https://platform.openai.com/
    echo.
    pause
)

cd ..

REM Frontend setup
echo.
echo 📦 Setting up frontend...
cd frontend

if not exist "node_modules" (
    echo   → Installing Node.js dependencies...
    call npm install --silent
) else (
    echo   → Dependencies already installed
)

cd ..

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║              ✅ Setup Complete!                           ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo 🚀 To start the application, run:
echo.
echo    start.bat
echo.
echo Then open your browser to: http://localhost:3000
echo.
echo 📚 For more information:
echo    • Quick reference: CHECKLIST.md
echo    • Setup details: SETUP.md
echo    • Usage examples: EXAMPLES.md
echo.
echo Happy wellness advising! 🏥
echo.
pause
