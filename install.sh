#!/bin/bash
# Thai Learning App - AI Installation Script
# This script automates the file setup

echo "=============================================="
echo "🪷 Thai Learning App - AI Setup"
echo "=============================================="
echo ""

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: app.py not found!"
    echo "   Please run this script from your project root directory"
    echo "   (the directory containing app.py)"
    exit 1
fi

echo "✅ Found app.py"
echo ""

# Check if templates directory exists
if [ ! -d "templates" ]; then
    echo "📁 Creating templates/ directory..."
    mkdir templates
fi

echo "✅ Templates directory ready"
echo ""

# Backup existing files
echo "💾 Creating backups..."
if [ -f "app.py" ]; then
    cp app.py app.py.backup
    echo "   ✓ Backed up app.py → app.py.backup"
fi

if [ -f "templates/base.html" ]; then
    cp templates/base.html templates/base.html.backup
    echo "   ✓ Backed up base.html → base.html.backup"
fi

echo ""

# Check if downloaded files exist
echo "🔍 Checking for downloaded AI files..."

if [ ! -f "ai_agent.py" ]; then
    echo "❌ ai_agent.py not found!"
    echo "   Please download ai_agent.py from the outputs and place it here"
    exit 1
fi
echo "   ✓ Found ai_agent.py"

if [ ! -f "chat.html" ]; then
    echo "❌ chat.html not found!"
    echo "   Please download chat.html from the outputs and place it here"
    exit 1
fi
echo "   ✓ Found chat.html"

echo ""

# Move files to correct locations
echo "📦 Installing files..."

# chat.html goes to templates
cp chat.html templates/chat.html
echo "   ✓ Installed chat.html → templates/chat.html"

# Check if user wants to replace app.py and base.html
echo ""
echo "⚠️  IMPORTANT DECISION:"
echo ""
echo "Do you want to:"
echo "  1) Replace your app.py with the AI-integrated version (RECOMMENDED)"
echo "  2) Keep your current app.py (you'll need to manually add AI code)"
echo ""
read -p "Enter 1 or 2: " choice

if [ "$choice" = "1" ]; then
    # Check if the integrated app.py exists
    if [ -f "app_integrated.py" ]; then
        cp app_integrated.py app.py
        echo "   ✓ Replaced app.py with AI-integrated version"
        echo "   ℹ️  Your old app.py is backed up as app.py.backup"
    else
        echo "   ⚠️  app_integrated.py not found"
        echo "   Please download 'app.py' from outputs and rename your current app.py first"
    fi
else
    echo "   ℹ️  Keeping your current app.py"
    echo "   You'll need to manually add the AI code (see ai_integration.py)"
fi

echo ""
echo "❓ Replace templates/base.html with AI-enhanced version?"
echo "   (Adds 🤖 AI Chat link to navigation)"
read -p "Replace base.html? (y/n): " replace_base

if [ "$replace_base" = "y" ] || [ "$replace_base" = "Y" ]; then
    if [ -f "base.html" ]; then
        cp base.html templates/base.html
        echo "   ✓ Replaced templates/base.html"
        echo "   ℹ️  Your old base.html is backed up as base.html.backup"
    else
        echo "   ⚠️  base.html not found in current directory"
    fi
else
    echo "   ℹ️  Keeping your current base.html"
    echo "   You can manually add: <li><a href=\"/chat\">🤖 AI Chat</a></li>"
fi

echo ""
echo "=============================================="
echo "📋 NEXT STEPS:"
echo "=============================================="
echo ""
echo "1. Install the Anthropic package:"
echo "   pip install anthropic --break-system-packages"
echo ""
echo "2. Get your API key:"
echo "   → Visit: https://console.anthropic.com"
echo "   → Create an API key"
echo "   → Copy it (starts with sk-ant-...)"
echo ""
echo "3. Set your API key:"
echo "   export ANTHROPIC_API_KEY='sk-ant-your-key-here'"
echo ""
echo "4. Run your app:"
echo "   python app.py"
echo ""
echo "5. Visit: http://localhost:5000/chat"
echo ""
echo "=============================================="
echo "✅ File setup complete!"
echo "=============================================="
echo ""
echo "📖 For detailed instructions, see:"
echo "   - QUICK_START.md (5-minute guide)"
echo "   - PHASE_1_SETUP_GUIDE.md (complete guide)"
echo ""
