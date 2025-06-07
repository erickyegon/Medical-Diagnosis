#!/bin/bash
# Render build script for frontend

set -e

echo "🎨 Installing frontend dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "🔍 Verifying installation..."
python -c "import streamlit, requests; print('✅ Core dependencies installed')"

echo "📁 Creating Streamlit config..."
mkdir -p ~/.streamlit
cat > ~/.streamlit/config.toml << EOF
[server]
headless = true
port = 8501
address = "0.0.0.0"
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
EOF

echo "📁 Creating necessary directories..."
mkdir -p /opt/render/project/src/data

echo "✅ Frontend build completed successfully!"
