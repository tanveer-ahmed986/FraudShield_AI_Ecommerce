@echo off
REM Quick deployment script for fraud detection system (Windows)

echo ================================
echo Fraud Detection System
echo Production Deployment Checklist
echo ================================
echo.

REM Check if git is initialized
if not exist .git (
    echo [*] Initializing git repository...
    git init
    git add .
    git commit -m "Initial commit - Production deployment setup"
)

REM Check if remote exists
git remote >nul 2>&1
if errorlevel 1 (
    echo [X] No git remote configured.
    echo Please create a GitHub repository and run:
    echo   git remote add origin https://github.com/YOUR-USERNAME/fraud-detection-system.git
    echo   git push -u origin main
    goto :end
)

echo [OK] Git repository ready
echo.

REM Frontend
echo [1] Frontend Deployment (Vercel)
echo --------------------------------
where vercel >nul 2>&1
if errorlevel 1 (
    echo [ ] Vercel CLI not installed
    echo     Install: npm install -g vercel
) else (
    echo [OK] Vercel CLI installed
    echo     Run: cd frontend ^&^& vercel --prod
)
echo.

REM Backend
echo [2] Backend Deployment (Render)
echo --------------------------------
echo [ ] Push code: git push origin main
echo [ ] Create web service: https://dashboard.render.com/new/web
echo [ ] Configure (see DEPLOYMENT.md)
echo.

REM Database
echo [3] Database Setup (Supabase)
echo ----------------------------
echo [ ] Create project: https://app.supabase.com
echo [ ] Copy connection string
echo [ ] Add to Render environment
echo.

REM Plugin
echo [4] WooCommerce Plugin
echo ----------------------
if exist "plugin\woo-fraud-detect.zip" (
    echo [OK] Plugin ready: plugin\woo-fraud-detect.zip
) else (
    echo [ ] Package plugin (already done if woo-fraud-detect.zip exists)
)
echo.

:end
echo ===================================
echo Full guide: DEPLOYMENT.md
echo ===================================
pause
