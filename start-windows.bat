@echo off
echo Python:
echo cd python-analysis
echo python -m venv .venv
echo .venv\Scripts\activate
echo pip install -r requirements.txt
echo python seed_data.py
echo uvicorn main:app --reload --port 8000
echo.
echo Spring Boot:
echo cd spring-backend
echo mvn spring-boot:run
echo.
echo React:
echo cd frontend
echo npm install
echo npm run dev
pause
