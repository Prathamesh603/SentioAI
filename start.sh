#!/bin/bash
# Render deployment startup script
# This script ensures proper setup before running the app

set -e

echo "=========================================="
echo "Sentiment Analysis Chatbot - Render Deploy"
echo "=========================================="
echo ""

echo "📦 Installing dependencies..."
pip install -q -r requirements.txt

echo "✅ Dependencies installed"
echo ""

echo "🚀 Starting Streamlit application..."
echo "App will be available at https://your-app-name.onrender.com"
echo ""

# Run Streamlit with proper configuration for Render
streamlit run dashboard/main.py \
  --server.port=$PORT \
  --server.address=0.0.0.0 \
  --server.headless=true \
  --logger.level=info
