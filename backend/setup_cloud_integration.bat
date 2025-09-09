@echo off
echo 🚀 Setting up N8N Cloud Integration for Hedge Funder
echo ====================================================

echo 📋 Prerequisites Check:
echo 1. Make sure your backend is running: python n8n_api.py
echo 2. Make sure ngrok is installed: npm install -g ngrok
echo 3. Make sure you have your ngrok auth token
echo.

pause

echo 🔧 Step 1: Starting automated setup...
python setup_n8n_cloud.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ Automated setup completed successfully!
    echo.
    echo 📋 Manual Steps Remaining:
    echo 1. Go to https://ash1industries.app.n8n.cloud
    echo 2. Import the generated n8n_workflow_template.json
    echo 3. Test the workflow manually
    echo 4. Configure Telegram bot (optional)
    echo 5. Enable automatic scheduling
    echo.
    echo 📚 For detailed instructions, see:
    echo    N8N_CLOUD_SETUP_GUIDE.md
    echo.
    echo 🎉 Your N8N cloud is now linked with your local backend!
) else (
    echo.
    echo ❌ Automated setup failed.
    echo Please check the errors above and try again.
    echo You can also follow the manual setup guide in N8N_CLOUD_SETUP_GUIDE.md
)

echo.
pause
