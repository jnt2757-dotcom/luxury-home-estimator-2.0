from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

app = FastAPI()

# Serve static files (CSS, JS, images)
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Serve index.html at root
@app.get("/")
async def root():
    return FileResponse("frontend/index.html")

# Enable CORS so frontend JS can call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model for detailed estimate
class EstimateRequest(BaseModel):
    square_feet: int
    bedrooms: int
    bathrooms: int
    floors: int
    basement: bool
    garage_cars: int
    home_style: str
    roof_type: str
    exterior_finish: str
    windows_type: str
    flooring: str
    kitchen_type: str
    countertops: str
    appliances: str
    bathroom_finish: str
    solar: bool
    smart_home: str
    insulation: str
    neighborhood: str
    lot_size: float
    landscaping: str
    pool: bool
    deck: bool
    outdoor_kitchen: bool
    extras: list[str] = []

# Example Charlotte NC luxury home cost calculation
@app.post("/estimate")
async def get_estimate(request: EstimateRequest):
    base_cost_per_sqft = 350  # Charlotte luxury base
    cost = request.square_feet * base_cost_per_sqft
    cost += request.bedrooms * 5000
    cost += request.bathrooms * 3000
    cost += request.floors * 10000
    cost += request.garage_cars * 8000
    cost += 20000 if request.basement else 0
    cost += 50000 if request.pool else 0
    cost += 10000 if request.deck else 0
    cost += 15000 if request.outdoor_kitchen else 0

    # Finish upgrades
    finish_multiplier = 1.0
    if request.flooring.lower() in ["hardwood", "marble", "tile"]:
        finish_multiplier += 0.05
    if request.kitchen_type.lower() == "gourmet":
        finish_multiplier += 0.1
    if request.countertops.lower() in ["quartz", "marble"]:
        finish_multiplier += 0.05
    if request.appliances.lower() == "high-end":
        finish_multiplier += 0.05
    if request.bathroom_finish.lower() == "luxury":
        finish_multiplier += 0.05
    cost *= finish_multiplier

    # Neighborhood modifier
    neighborhood_modifiers = {
        "uptown": 1.1,
        "southpark": 1.05,
        "ballantyne": 1.05,
        "suburban": 1.0,
        "rural": 0.95
    }
    cost *= neighborhood_modifiers.get(request.neighborhood.lower(), 1.0)

    # Solar / smart home / insulation bonuses
    if request.solar:
        cost += 20000
    if request.smart_home.lower() == "full":
        cost += 15000
    if request.insulation.lower() == "high-efficiency":
        cost += 5000

    return {"estimate": round(cost, 2)}
