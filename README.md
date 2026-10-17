# Placement Prediction & Statistical Analysis System

Full-stack academic project using React, Spring Boot, PostgreSQL and Python.

Architecture:
React -> Spring Boot -> PostgreSQL
                    -> Python FastAPI statistical service -> Spring Boot -> React

Python performs descriptive statistics, correlation, conditional probability,
hypothesis testing and logistic-regression placement prediction.

Requirements:
- Java 17+
- Maven 3.9+
- Python 3.10+
- Node.js 18+
- PostgreSQL 14+

Run:
1. Create PostgreSQL database `placement_prediction`.
2. Run `database/schema.sql`.
3. In `python-analysis`:
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   python seed_data.py
   uvicorn main:app --reload --port 8000
4. Open `spring-backend` in IntelliJ and run `PlacementPredictionApplication`,
   or `mvn spring-boot:run`.
5. In `frontend`:
   npm install
   npm run dev
6. Open http://localhost:5173

Default PostgreSQL credentials are postgres/postgres. Change them in:
- python-analysis/config.py
- spring-backend/src/main/resources/application.properties

Main Spring APIs:
GET  /api/students
POST /api/students
GET  /api/analytics/overview
GET  /api/analytics/correlations
GET  /api/analytics/probabilities
GET  /api/analytics/hypothesis
POST /api/predict

The seed data is synthetic development data for the academic project.
