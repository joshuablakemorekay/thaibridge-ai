@echo off
REM Thai Learning App - AI Installation Script (Windows)
REM This script automates the file setup

echo ==============================================
echo 🪷 Thai Learning App - AI Setup (Windows)
echo ==============================================
echo.

REM Check if we're in the right directory
if not exist "app.py" (
    echo ❌ Error: app.py not found!
    echo    Please run this script from your project root directory
    echo    the directory containing app.py
    pause
    exit /b 1
)

echo ✅ Found app.py
echo.

REM Check if templates directory exists
if not exist "templates" (
    echo 📁 Creating templates\ directory...
    mkdir templates
)

echo ✅ Templates directory ready
echo.

REM Backup existing files
echo 💾 Creating backups...
if exist "app.py" (
    copy app.py app.py.backup >nul
    echo    ✓ Backed up app.py to app.py.backup
)

if exist "templates\base.html" (
    copy templates\base.html templates\base.html.backup >nul
    echo    ✓ Backed up base.html to base.html.backup
)

echo.

REM Check if downloaded files exist
echo 🔍 Checking for downloaded AI files...

if not exist "ai_agent.py" (
    echo ❌ ai_agent.py not found!
    echo    Please download ai_agent.py from the outputs and place it here
    pause
    exit /b 1
)
echo    ✓ Found ai_agent.py

if not exist "chat.html" (
    echo ❌ chat.html not found!
    echo    Please download chat.html from the outputs and place it here
    pause
    exit /b 1
)
echo    ✓ Found chat.html

echo.

REM Move files to correct locations
echo 📦 Installing files...

REM chat.html goes to templates
copy chat.html templates\chat.html >nul
echo    ✓ Installed chat.html to templates\chat.html

REM Ask about replacing app.py
echo.
echo ⚠️  IMPORTANT DECISION:
echo.
echo Do you want to:
echo   1 Replace your app.py with the AI-integrated version (RECOMMENDED)
echo   2 Keep your current app.py (you'll need to manually add AI code)
echo.
set /p choice="Enter 1 or 2: "

if "%choice%"=="1" (
    if exist "app_integrated.py" (
        copy app_integrated.py app.py >nul
        echo    ✓ Replaced app.py with AI-integrated version
        echo    ℹ️  Your old app.py is backed up as app.py.backup
    ) else (
        echo    ⚠️  The integrated app.py file was not found
        echo    Please download 'app.py' from outputs
    )
) else (
    echo    ℹ️  Keeping your current app.py
    echo    You'll need to manually add the AI code (see ai_integration.py)
)

echo.
echo ❓ Replace templates\base.html with AI-enhanced version?
echo    (Adds 🤖 AI Chat link to navigation)
set /p replace_base="Replace base.html? (y/n): "

if /i "%replace_base%"=="y" (
    if exist "base.html" (
        copy base.html templates\base.html >nul
        echo    ✓ Replaced templates\base.html
        echo    ℹ️  Your old base.html is backed up as base.html.backup
    ) else (
        echo    ⚠️  base.html not found in current directory
    )
) else (
    echo    ℹ️  Keeping your current base.html
    echo    You can manually add: ^<li^>^<a href="/chat"^>🤖 AI Chat^</a^>^</li^>
)

echo.
echo ==============================================
echo 📋 NEXT STEPS:
echo ==============================================
echo.
echo 1. Install the Anthropic package:
echo    pip install anthropic --break-system-packages
echo.
echo 2. Get your API key:
echo    Visit: https://console.anthropic.com
echo    Create an API key
echo    Copy it (starts with sk-ant-...)
echo.
echo 3. Set your API key (PowerShell):
echo    $env:ANTHROPIC_API_KEY = "sk-ant-your-key-here"
echo.
echo    OR (Command Prompt):
echo    set ANTHROPIC_API_KEY=sk-ant-your-key-here
echo.
echo 4. Run your app:
echo    python app.py
echo.
echo 5. Visit: http://localhost:5000/chat
echo.
echo ==============================================
echo ✅ File setup complete!
echo ==============================================
echo.
echo 📖 For detailed instructions, see:
echo    - QUICK_START.md (5-minute guide)
echo    - PHASE_1_SETUP_GUIDE.md (complete guide)
echo.
pause
