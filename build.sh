#!/bin/bash
# Force Python 3.12 and build
set -e

echo "=========================================="
echo "Build Script: Sentiment Analysis Chatbot"
echo "=========================================="

# Check Python version
python --version
echo ""

# Ensure we're using Python 3.12+
if python -c 'import sys; exit(0 if sys.version_info >= (3, 12) else 1)'; then
    echo "✅ Python version is 3.12 or higher"
else
    echo "❌ ERROR: Python must be 3.12 or higher"
    exit 1
fi

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Build completed successfully"
