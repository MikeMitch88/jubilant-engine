#!/bin/bash
# Render Backend Startup Script for FastAPI

set -e

echo "Starting Codebase Genius Backend API..."
echo "Python version: $(python --version)"
echo "Port: ${PORT:-8000}"

# Create outputs directory if it doesn't exist
mkdir -p outputs

# Start the FastAPI server
exec uvicorn server:app --host 0.0.0.0 --port ${PORT:-8000}
