#!/bin/bash

# start_all.sh - Script to start all stacks (Backend & Frontend)
# This script handles dependency installation and starts both services concurrently.

# Set colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Starting TodoList Application Stacks...${NC}"

# Function to handle cleanup on exit
cleanup() {
    echo -e "\n${RED}🛑 Stopping all services...${NC}"
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit
}

trap cleanup SIGINT SIGTERM EXIT

# 1. Setup Backend (FastAPI)
echo -e "${GREEN}📦 Setting up Backend (FastAPI)...${NC}"
cd backend || exit

# Check if virtual environment exists, if not create it
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install requirements
echo "Installing Python dependencies..."
pip install -r requirements.txt --quiet

# Start Backend in background
echo -e "${BLUE}📡 Starting Backend on http://localhost:8000...${NC}"
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

cd ..

# 2. Setup Frontend (Electron + Vite)
echo -e "${GREEN}📦 Setting up Frontend (Electron)...${NC}"
cd desktop || exit

# Install npm dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "Installing Node dependencies..."
    npm install
fi

# Start Frontend in background
echo -e "${BLUE}💻 Starting Frontend...${NC}"
# We use 'npm run dev' which starts both Vite (React) and Electron
npm run dev &
FRONTEND_PID=$!

# 3. Wait for processes
echo -e "${GREEN}✅ All stacks are starting! Press Ctrl+C to stop everything.${NC}"
wait
