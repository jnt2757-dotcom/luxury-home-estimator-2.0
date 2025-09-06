from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# Allow frontend JS to call API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

NEIGHBORHOODS = ["Eastover", "Foxcroft", "Myers Park"]

@app.get("/")
async def home():
    return FileResponse(os.path.join("frontend", "index.html"))

@app.post("/estimate")
async def estimate(data: dict):
    # General
    sqft = int(data.get("sqft", 0))
    bedrooms = int(data.get("bedrooms", 0))
    bathrooms = int(data.get("bathrooms", 0))
    garage = int(data.get("garage", 0))

    # Luxury Features
    pool = data.get("pool", "No")
    spa = data.get("spa", "No")
    theater = data.get("theater", "No")
    elevator = data.get("elevator", "No")
    wine_cellar = data.get("wine_cellar", "No")
    outdoor_kitchen = data.get("outdoor_kitchen", "No")

    # Kitchen & Interiors
    kitchen = data.get("kitchen", "Standard")
    flooring = data.get("flooring", "Carpet")
    cabinetry = data.get("cabinetry", "Standard")
    countertops = data.get("countertops", "Granite")

    # Base Costs
    base_cost_per_sqft = 650
    bedroom_cost = 15000
    bathroom_cost = 10000
    garage_cost = 10000 * garage

    # Luxury add-ons costs
    pool_cost = 100000 if pool=="Yes" else 0
    spa_cost = 15000 if spa=="Yes" else 0
    theater_cost = 25000 if theater=="Yes" else 0
    elevator_cost = 50000 if elevator=="Yes" else 0
    wine_cellar_cost = 20000 if wine_cellar=="Yes" else 0
    outdoor_kitchen_cost = 30000 if outdoor_kitchen=="Yes" else 0

    kitchen_cost = 20000 if kitchen=="Premium" else 0
    flooring_cost = 15000 if flooring=="Hardwood" else 0
    cabinetry_cost = 15000 if cabinetry=="Custom" else 0
    countertop_cost = 10000 if countertops=="Quartz" else 0

    total_estimate = (
        sqft * base_cost_per_sqft
        + bedrooms * bedroom_cost
        + bathrooms * bathroom_cost
        + garage_cost
        + pool_cost + spa_cost + theater_cost + elevator_cost + wine_cellar_cost + outdoor_kitchen_cost
        + kitchen_cost + flooring_cost + cabinetry_cost + countertop_cost
    )

    summary = {
        "sqft": sqft,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "garage": garage,
        "pool": pool,
        "spa": spa,
        "theater": theater,
        "elevator": elevator,
        "wine_cellar": wine_cellar,
        "outdoor_kitchen": outdoor_kitchen,
        "kitchen": kitchen,
        "flooring": flooring,
        "cabinetry": cabinetry,
        "countertops": countertops,
        "total_estimate": f"${total_estimate:,}"
    }

    return JSONResponse(summary)
