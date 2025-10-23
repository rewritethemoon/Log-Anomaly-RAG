@echo off
echo ========================================
echo   LOG ANOMALY RAG ASSISTANT - STARTING
echo ========================================
echo.

:: Kiểm tra Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found! Please install Python 3.10+
    pause
    exit /b
)

:: Kiểm tra pip install
echo Installing dependencies...
pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install packages!
    pause
    exit /b
)

:: Chạy API trên port 8001
start "API Server" cmd /k "python api/main.py"

:: Đợi 3 giây
timeout /t 3 >nul

:: Chạy Streamlit
start "Web Demo" cmd /k "streamlit run app.py --server.port=8501"

:: Mở trình duyệt
timeout /t 2 >nul
start http://localhost:8501

echo.
echo ========================================
echo    SYSTEM READY! 
echo    API: http://127.0.0.1:8001
echo    Demo: http://localhost:8501
echo ========================================
echo Press any key to EXIT...
pause >nul