#!/bin/bash

# Codebase Genius Startup Script
# This script helps start all components of the system

set -e

echo "🧠 Codebase Genius - Startup Script"
echo "===================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if virtual environment is activated
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo -e "${RED}❌ Virtual environment not activated!${NC}"
    echo "Please run: source venv/bin/activate"
    exit 1
fi

echo -e "${GREEN}✅ Virtual environment active${NC}"
echo ""

# Function to check if a port is in use
port_in_use() {
    lsof -i :$1 >/dev/null 2>&1
    return $?
}

# Check ports
if port_in_use 8000; then
    echo -e "${BLUE}ℹ️  Port 8000 already in use (API might be running)${NC}"
else
    echo -e "${GREEN}✅ Port 8000 available${NC}"
fi

if port_in_use 8501; then
    echo -e "${BLUE}ℹ️  Port 8501 already in use (Streamlit might be running)${NC}"
else
    echo -e "${GREEN}✅ Port 8501 available${NC}"
fi

echo ""
echo "Select startup mode:"
echo "1) Full system (API + UI) - Recommended"
echo "2) API only"
echo "3) UI only (requires API running)"
echo "4) Run tests"
echo "5) Exit"
echo ""

read -p "Enter choice [1-5]: " choice

case $choice in
    1)
        echo ""
        echo -e "${GREEN}🚀 Starting Full System...${NC}"
        echo ""
        echo "This will start:"
        echo "  - FastAPI server on http://localhost:8000"
        echo "  - Streamlit UI on http://localhost:8501"
        echo ""
        echo "Press Ctrl+C to stop all services"
        echo ""
        sleep 2
        
        # Start API in background
        echo -e "${BLUE}Starting API server...${NC}"
        uvicorn server:app --host 0.0.0.0 --port 8000 &
        API_PID=$!
        
        # Wait for API to be ready
        sleep 3
        
        # Start Streamlit
        echo -e "${BLUE}Starting Streamlit UI...${NC}"
        streamlit run app.py
        
        # Kill API when Streamlit stops
        kill $API_PID 2>/dev/null || true
        ;;
        
    2)
        echo ""
        echo -e "${GREEN}🚀 Starting API Server...${NC}"
        echo ""
        echo "API will be available at:"
        echo "  - http://localhost:8000"
        echo "  - API docs: http://localhost:8000/docs"
        echo ""
        uvicorn server:app --host 0.0.0.0 --port 8000 --reload
        ;;
        
    3)
        echo ""
        echo -e "${GREEN}🚀 Starting Streamlit UI...${NC}"
        echo ""
        echo "Make sure API server is running on port 8000"
        echo "UI will be available at http://localhost:8501"
        echo ""
        sleep 2
        streamlit run app.py
        ;;
        
    4)
        echo ""
        echo -e "${GREEN}🧪 Running Tests...${NC}"
        echo ""
        python test_setup.py
        ;;
        
    5)
        echo "Goodbye! 👋"
        exit 0
        ;;
        
    *)
        echo -e "${RED}Invalid choice${NC}"
        exit 1
        ;;
esac
