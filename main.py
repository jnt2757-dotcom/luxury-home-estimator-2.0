from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Thompson Custom Building Group - Luxury Home Estimator")

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class EstimateRequest(BaseModel):
    squareFeet: int
    bedrooms: int
    bathrooms: int
    homeStyle: str
    neighborhood: str
    pool: bool
    poolType: str = ""
    garage: str
    basement: bool
    smartHome: str
    wineCellar: bool
    gym: bool
    elevator: bool
    landscaping: str

@app.post("/estimate")
def get_estimate(data: EstimateRequest):
    # Base cost per sq ft
    base_price = 400  

    # Home style multiplier
    style_multiplier = {
        "Modern": 1.05,
        "Colonial": 1.0,
        "Craftsman": 1.03
    }.get(data.homeStyle, 1.0)

    # Neighborhood multiplier
    neighborhood_multiplier = {
        "Eastover": 1.2,
        "Foxcroft": 1.15,
        "Myers Park": 1.25
    }.get(data.neighborhood, 1.0)

    # Optional extras
    extras = 0
    if data.pool:
        extras += {"Infinity": 120000, "Lap": 80000, "Standard": 50000}.get(data.poolType, 0)
    if data.basement:
        extras += 50000
    if data.smartHome == "Full":
        extras += 30000
    if data.wineCellar:
        extras += 40000
    if data.gym:
        extras += 25000
    if data.elevator:
        extras += 60000
    if data.landscaping == "Full":
        extras += 35000

    # Calculate final estimate
    estimate = (data.squareFeet * base_price * style_multiplier * neighborhood_multiplier) + extras

    return {"estimate": round(estimate, 2)}
