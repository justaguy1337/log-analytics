#!/bin/bash

# Log Analytics Platform - Startup Script

echo "🚀 Starting Distributed Log Analytics Platform..."
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if backend and frontend directories exist
if [ ! -d "$PROJECT_ROOT/backend" ] || [ ! -d "$PROJECT_ROOT/frontend" ]; then
    echo -e "${RED}Error: Backend or frontend directory not found${NC}"
    echo "Expected: $PROJECT_ROOT/backend and $PROJECT_ROOT/frontend"
    exit 1
fi

# Check if venv exists
if [ ! -d "$PROJECT_ROOT/venv" ]; then
    echo -e "${RED}Error: Virtual environment not found at $PROJECT_ROOT/venv${NC}"
    echo "Please create it first:"
    echo "  cd $PROJECT_ROOT && python -m venv venv"
    exit 1
fi

# Activate virtual environment
cd "$PROJECT_ROOT"
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to activate virtual environment${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Virtual environment activated${NC}"
echo ""

# Start backend in background (run from project root for proper module imports)
echo -e "${BLUE}Starting Backend Server...${NC}"
cd "$PROJECT_ROOT"
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to start backend${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Backend started (PID: $BACKEND_PID)${NC}"
sleep 2

# Start frontend in background
echo -e "${BLUE}Starting Frontend Server...${NC}"
cd "$PROJECT_ROOT/frontend"
npm run dev &
FRONTEND_PID=$!
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to start frontend${NC}"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi
echo -e "${GREEN}✓ Frontend started (PID: $FRONTEND_PID)${NC}"
sleep 2

echo ""
echo -e "${GREEN}✓ Platform is running!${NC}"
echo ""
echo "📊 Dashboard: http://localhost:5173"
echo "🔌 API: http://localhost:8000"
echo "📖 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Trap to kill both processes on exit
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" SIGINT SIGTERM

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID
