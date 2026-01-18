#!/bin/bash

# AI Doctor - Quick Start Script
# This script helps you set up the application quickly

echo "╔════════════════════════════════════════════════════════════╗"
echo "║        🏥 AI Doctor - Quick Setup Assistant              ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check Python
echo "🔍 Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi
PYTHON_VERSION=$(python3 --version | cut -d ' ' -f 2)
echo "✅ Python $PYTHON_VERSION found"
echo ""

# Check Node
echo "🔍 Checking Node.js installation..."
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16 or higher."
    exit 1
fi
NODE_VERSION=$(node --version)
echo "✅ Node.js $NODE_VERSION found"
echo ""

# Backend setup
echo "📦 Setting up backend..."
cd backend

if [ ! -d "venv" ]; then
    echo "  → Creating virtual environment..."
    python3 -m venv venv
fi

echo "  → Activating virtual environment..."
source venv/bin/activate

echo "  → Installing Python dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

if [ ! -f ".env" ]; then
    echo "  → Creating .env file..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Please add your OpenAI API key to backend/.env"
    echo "   Edit the file and replace 'your_openai_api_key_here' with your actual key"
    echo "   Get your key from: https://platform.openai.com/"
    echo ""
    read -p "Press Enter once you've added your API key to continue..."
fi

cd ..

# Frontend setup
echo ""
echo "📦 Setting up frontend..."
cd frontend

if [ ! -d "node_modules" ]; then
    echo "  → Installing Node.js dependencies..."
    npm install --silent
else
    echo "  → Dependencies already installed"
fi

cd ..

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║              ✅ Setup Complete!                           ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "🚀 To start the application, run:"
echo ""
echo "   ./start.sh"
echo ""
echo "Then open your browser to: http://localhost:3000"
echo ""
echo "📚 For more information:"
echo "   • Quick reference: CHECKLIST.md"
echo "   • Setup details: SETUP.md"
echo "   • Usage examples: EXAMPLES.md"
echo ""
echo "Happy wellness advising! 🏥"
