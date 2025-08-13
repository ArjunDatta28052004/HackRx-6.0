# 🚀 Quick Start Guide

Get the Insurance Query System up and running in 5 minutes!

## Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

## Quick Setup

### Option 1: Automated Setup (Recommended)

```bash
# Make the startup script executable and run it
chmod +x start.sh
./start.sh
```

This will:
- ✅ Install all Python dependencies
- ✅ Download spaCy models
- ✅ Install frontend dependencies
- ✅ Create necessary directories
- ✅ Start the backend server

### Option 2: Manual Setup

#### Backend Setup
```bash
# Install Python dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Start backend
python app.py
```

#### Frontend Setup (in new terminal)
```bash
cd frontend
npm install
npm start
```

## Access the Application

- 🌐 **Frontend**: http://localhost:3000
- 📡 **Backend API**: http://localhost:5000

## First Steps

1. **Register Account**: Create a new user account
2. **Upload Documents**: Go to Documents page and upload PDF/DOCX files
3. **Build Index**: Click "Build Index" to process your documents
4. **Ask Questions**: Use the Query page to ask insurance-related questions

## Example Query

Try this example query:
> "A 45-year-old male from Mumbai needs knee surgery with a 2-year policy"

## Need Help?

- Check the main [README.md](README.md) for detailed documentation
- Review the troubleshooting section
- Open an issue on GitHub

## Development

For development with hot reloading:

```bash
# Backend (auto-reloads on changes)
export FLASK_ENV=development
python app.py

# Frontend (auto-reloads on changes)
cd frontend
npm start
```

Happy coding! 🎉