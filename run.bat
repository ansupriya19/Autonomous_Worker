@echo off
cd /d "%~dp0"
if not exist .venv\Scripts\python.exe (echo Run setup.bat first.&pause&exit /b 1)
if not exist .env copy .env.example .env
start "Worker API" cmd /k "call .venv\Scripts\activate && python -m uvicorn app.main:app --host 127.0.0.1 --port 8000"
timeout /t 3 /nobreak >nul
call .venv\Scripts\activate
python -m streamlit run streamlit_app.py --server.address 127.0.0.1 --server.port 8502
