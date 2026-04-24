#!/bin/bash
# MedAssistant - Startup Script

set -e

echo ""
echo "╔════════════════════════════════════════╗"
echo "║        MedAssistant Startup            ║"
echo "╚════════════════════════════════════════╝"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
  echo "❌ Python 3 is required but not installed."
  exit 1
fi

# Check API key
if [ -z "$ANTHROPIC_API_KEY" ]; then
  echo "❌ ANTHROPIC_API_KEY environment variable is not set."
  echo ""
  echo "  Export it first:"
  echo "  export ANTHROPIC_API_KEY=sk-ant-..."
  echo ""
  exit 1
fi

echo "✅ Anthropic API key found"

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip install -r backend/requirements.txt -q

echo ""
echo "🚀 Starting MedAssistant API server..."
echo ""
echo "  API:      http://localhost:8000"
echo "  UI:       http://localhost:8000"
echo "  API Docs: http://localhost:8000/docs"
echo ""
echo "  Press Ctrl+C to stop."
echo ""

# Run backend (serves frontend as static files)
cd backend
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
