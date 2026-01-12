#!/bin/bash
# Quick setup script for Trace documentation site

set -e

echo "🚀 Setting up Trace Documentation Site..."
echo ""

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: Please run this script from the trace-docs directory"
    exit 1
fi

# Check if Trace repo exists
if [ ! -d "../Trace" ]; then
    echo "⚠️  Warning: Trace repository not found at ../Trace"
    echo "   Automation scripts may not work without it."
    echo ""
fi

# Install Node dependencies
echo "📦 Installing Node.js dependencies..."
if command -v yarn &> /dev/null; then
    yarn install
else
    npm install
fi

# Make Python scripts executable
echo "🔧 Making Python scripts executable..."
chmod +x scripts/generate_api_docs.py
chmod +x scripts/convert_notebooks.py

echo ""
echo "✨ Setup complete!"
echo ""
echo "📋 Available commands:"
echo "   npm run dev                    - Start development server"
echo "   npm run build                  - Build for production"
echo "   npm run docs:generate-api      - Generate API documentation"
echo "   npm run docs:convert-notebooks - Convert Jupyter notebooks"
echo "   npm run docs:generate-all      - Run all generators"
echo ""
echo "🎉 Ready to go! Run 'npm run dev' to start."

