#!/bin/bash

echo "🚀 Starting Insurance Query System..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+ first."
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm first."
    exit 1
fi

echo "✅ Prerequisites check passed!"

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Download spaCy model if not exists
echo "🧠 Setting up spaCy model..."
python -m spacy download en_core_web_sm

# Install frontend dependencies
echo "📱 Installing frontend dependencies..."
cd frontend
npm install
cd ..

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p uploads
mkdir -p faiss_index

# Set environment variables
export SECRET_KEY="your-secret-key-here-change-in-production"
export FLASK_ENV=development

echo "🎯 Starting backend server..."
echo "📡 Backend will run on: http://localhost:5000"
echo "🌐 Frontend will run on: http://localhost:3000"
echo ""
echo "💡 Open a new terminal and run: cd frontend && npm start"
echo ""

# Start backend
python app.py