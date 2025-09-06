from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

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

    # Luxury features
    pool = data.get("pool") == "Yes"
    spa = data.get("spa") == "Yes"
    elevator = data.get("elevator") == "Yes"
    home_theater = data.get("home_theater") == "Yes"
    gym = data.get("gym") == "Yes"
    wine_cellar = data.get("wine_cellar") == "Yes"
    smart_home = data.get("smart_home") == "Yes"

    # Kitchen & Dining
    gourmet_kitchen = data.get("gourmet_kitchen") == "Yes"
    island = data.get("island") == "Yes"
    premium_appliances = data.get("premium_appliances") == "Yes"
    countertops = data.get("countertops") == "Marble"

    # Outdoor Living
    patio = data.get("patio") == "Yes"
    outdoor_kitchen = data.get("outdoor_kitchen") == "Yes"
    landscaping = data.get("landscaping") == "Yes"
    fencing = data.get("fencing") == "Yes"

    # Interior Finishes
    flooring = data.get("flooring", "Carpet")
    lighting = data.get("lighting", "Standard")
    cabinetry = data.get("cabinetry", "Standard")
    bathroom_finish = data.get("bathroom_finish", "Standard")

    # Extras
    guest_house = data.get("guest_house") == "Yes"
    office = data.get("office") == "Yes"
    security_system = data.get("security_system") == "Yes"
    solar_panels = data.get("solar_panels") == "Yes"

    # Base costs
    total = 0
    total += sqft * 600
    total += bedrooms * 15000
    total += bathrooms * 10000
    total += garage * 10000

    # Add-ons
    for feature, cost in [
        (pool, 100000), (spa, 20000), (elevator, 40000),
        (home_theater, 35000), (gym, 25000), (wine_cellar, 20000),
        (smart_home, 30000), (gourmet_kitchen, 20000),
        (island, 5000), (premium_appliances, 15000),
        (patio, 10000), (outdoor_kitchen, 15000),
        (landscaping, 10000), (fencing, 5000),
        (guest_house, 60000), (office, 10000),
        (security_system, 8000), (solar_panels, 25000)
    ]:
        if feature:
            total += cost

    # Finishes
    if flooring == "Hardwood": total += 15000
    if flooring == "Marble": total += 25000
    if lighting == "Premium": total += 10000
    if cabinetry == "Premium": total += 15000
    if bathroom_finish == "Luxury": total += 20000

    return JSONResponse({"estimate": f"${total:,}"})
