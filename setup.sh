#!/bin/bash

# PolyRatings Data Collection Setup Script

echo "🚀 Setting up PolyRatings Data Collection..."

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p data/main
mkdir -p data/tracking
mkdir -p .github/workflows

# Install Python dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Make the script executable
chmod +x get_professor_ids.py

echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Test locally: python get_professor_ids.py"
echo "2. Commit and push to GitHub"
echo "3. The workflow will run daily at 6 AM UTC"
echo "4. Check Actions tab in GitHub to monitor runs"
echo ""
echo "📁 File structure:"
echo "  data/main/          - Current data (committed to git)"
echo "  data/tracking/      - Historical snapshots (ignored by git)"
echo "  .github/workflows/  - GitHub Actions configuration"
