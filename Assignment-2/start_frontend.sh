#!/bin/bash
# Render Frontend Startup Script for Streamlit

set -e

echo "Starting Codebase Genius Frontend UI..."
echo "Python version: $(python --version)"
echo "Port: ${PORT:-8501}"
echo "API URL: ${API_URL:-http://localhost:8000}"

# Start Streamlit
exec streamlit run app.py \
  --server.port=${PORT:-8501} \
  --server.address=0.0.0.0 \
  --server.headless=true \
  --server.enableCORS=false \
  --server.enableXsrfProtection=false
