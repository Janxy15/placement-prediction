from fastapi import FastAPI
from pydantic import BaseModel, Field
from analysis import overview, correlations, probabilities, hypothesis, predict

app = FastAPI(title="Placement Statistical Analysis Service", version="1.0")

class PredictionInput(BaseModel):
    cgpa: float = Field(ge=0, le=10)
    aptitude_score: float = Field(ge=0, le=100)
    coding_score: float = Field(ge=0, le=100)
    communication_score: float = Field(ge=0, le=100)
    projects: int = Field(ge=0)
    internships: int = Field(ge=0)
    certifications: int = Field(ge=0)
    attendance: float = Field(ge=0, le=100)
    backlogs: int = Field(ge=0)

@app.get("/health")
def health():
    return {"status": "UP"}

@app.get("/analysis/overview")
def get_overview():
    return overview()

@app.get("/analysis/correlations")
def get_correlations():
    return correlations()

@app.get("/analysis/probabilities")
def get_probabilities():
    return probabilities()

@app.get("/analysis/hypothesis")
def get_hypothesis():
    return hypothesis()

@app.post("/predict")
def get_prediction(payload: PredictionInput):
    return predict(payload.model_dump())
