#!/bin/bash
# Render build script for backend

set -e

echo "🔧 Installing backend dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "🔍 Verifying installation..."
python -c "import fastapi, uvicorn, langserve; print('✅ Core dependencies installed')"

echo "📁 Creating necessary directories..."
mkdir -p /opt/render/project/src/data
mkdir -p /opt/render/project/src/logs

echo "✅ Backend build completed successfully!"
