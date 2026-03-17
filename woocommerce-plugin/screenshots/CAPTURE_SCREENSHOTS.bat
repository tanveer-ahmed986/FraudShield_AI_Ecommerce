@echo off
echo ========================================
echo AI Fraud Detection - Screenshot Helper
echo ========================================
echo.
echo This script will open all HTML mockups in your browser.
echo Take screenshots as each one opens (Windows: Win+Shift+S)
echo.
echo Press any key to start opening mockups...
pause >nul

echo.
echo Opening mockup 1/5: Settings Page...
start "" "mockups\05-settings-page.html"
timeout /t 5 >nul

echo Opening mockup 2/5: Fraud Box - Legitimate...
start "" "mockups\15-fraud-box-legitimate.html"
timeout /t 5 >nul

echo Opening mockup 3/5: Fraud Box - Fraud Detected...
start "" "mockups\16-fraud-box-fraud.html"
timeout /t 5 >nul

echo Opening mockup 4/5: Bulk Check Page...
start "" "mockups\17-bulk-check-page.html"
timeout /t 5 >nul

echo Opening mockup 5/5: Results Summary...
start "" "mockups\22-results-summary.html"
timeout /t 2 >nul

echo.
echo ========================================
echo All mockups opened!
echo ========================================
echo.
echo Next steps:
echo 1. Screenshot each browser tab (Win+Shift+S)
echo 2. Save as PNG with corresponding numbers
echo    - 05-settings-page.png
echo    - 15-fraud-box-legitimate.png
echo    - 16-fraud-box-fraud.png
echo    - 17-bulk-check-page.png
echo    - 22-results-summary.png
echo 3. Place screenshots in USER_MANUAL.md
echo.
pause
