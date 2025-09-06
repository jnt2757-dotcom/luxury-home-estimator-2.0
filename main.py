from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class EstimateRequest(BaseModel):
    project_name: str
    square_feet: int
    stories: int
    neighborhood_multiplier: float
    architect_multiplier: float
    features: List[float]

@app.post("/estimate")
def estimate(data: EstimateRequest):
    base_per_sqft = 650
    base_cost = data.square_feet * base_per_sqft
    neighborhood_cost = base_cost * data.neighborhood_multiplier
    architect_cost = neighborhood_cost * data.architect_multiplier
    features_total = sum(data.features)
    total = architect_cost + features_total

    breakdown = {
        "Base Cost": base_cost,
        "Neighborhood Adjusted": neighborhood_cost,
        "Architect Adjusted": architect_cost,
        "Features": features_total,
        "Total": total
    }

    return {"project_name": data.project_name, "breakdown": breakdown, "total_estimate": total}
