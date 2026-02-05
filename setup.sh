#!/bin/bash

# TataCliq Scraper - Automated Setup Script
# This script sets up the complete environment for the scraper

echo "🛍️  TataCliq Scraper - Setup Script"
echo "===================================="
echo ""

# Check Python version
echo "📋 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "   Found Python $python_version"

# Check if pip is installed
echo ""
echo "📦 Checking pip..."
if ! command -v pip3 &> /dev/null; then
    echo "   ❌ pip3 not found. Please install pip3 first."
    exit 1
fi
echo "   ✅ pip3 is installed"

# Create virtual environment
echo ""
echo "🔧 Creating virtual environment..."
if [ -d "venv" ]; then
    echo "   ⚠️  Virtual environment already exists. Skipping..."
else
    python3 -m venv venv
    echo "   ✅ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "⚡ Activating virtual environment..."
source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null
echo "   ✅ Virtual environment activated"

# Upgrade pip
echo ""
echo "📈 Upgrading pip..."
pip install --upgrade pip --quiet
echo "   ✅ pip upgraded"

# Install dependencies
echo ""
echo "📥 Installing dependencies..."
echo "   This may take a few minutes..."
pip install -r requirements.txt --quiet
if [ $? -eq 0 ]; then
    echo "   ✅ All dependencies installed successfully"
else
    echo "   ❌ Error installing dependencies"
    exit 1
fi

# Create sample input file
echo ""
echo "📄 Creating sample input file..."
python3 create_sample.py
if [ $? -eq 0 ]; then
    echo "   ✅ sample_input.xlsx created"
else
    echo "   ⚠️  Could not create sample file"
fi

# Check if git is initialized
echo ""
echo "🔍 Checking Git repository..."
if [ -d ".git" ]; then
    echo "   ✅ Git repository already initialized"
else
    echo "   Initializing Git repository..."
    git init
    git branch -M main
    echo "   ✅ Git repository initialized"
fi

# Summary
echo ""
echo "✨ Setup Complete!"
echo "=================="
echo ""
echo "📋 Next Steps:"
echo ""
echo "1️⃣  Run the app locally:"
echo "   streamlit run app.py"
echo ""
echo "2️⃣  Test with sample data:"
echo "   Upload sample_input.xlsx in the app"
echo ""
echo "3️⃣  Deploy to Streamlit Cloud:"
echo "   - Push to GitHub:"
echo "     git add ."
echo "     git commit -m 'Initial commit'"
echo "     git remote add origin YOUR_REPO_URL"
echo "     git push -u origin main"
echo ""
echo "   - Deploy at: https://share.streamlit.io"
echo ""
echo "📚 Documentation:"
echo "   - Quick Start: QUICKSTART.md"
echo "   - Full Docs: README.md"
echo "   - Deployment: DEPLOYMENT.md"
echo ""
echo "Happy Scraping! 🎉"
