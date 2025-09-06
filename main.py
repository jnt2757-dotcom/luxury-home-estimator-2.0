from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI()
app.mount("/static", StaticFiles(directory="frontend"), name="static")
templates = Jinja2Templates(directory="frontend")

BASE_PRICE = 650  # per sqft

OPTIONS = {
    "Exterior": {
        "Pool": 0.12,
        "Spa": 0.08,
        "Outdoor Kitchen": 0.10,
        "Slate Roof": 0.07,
        "Wood Roof": 0.05,
        "Stone Accents": 0.06,
        "Custom Landscaping": 0.05,
        "Driveway Pavers": 0.03
    },
    "Interior": {
        "Marble Floors": 0.10,
        "Hardwood Floors": 0.06,
        "Custom Millwork": 0.07,
        "Smart Home Integration": 0.08,
        "Elevator": 0.12,
        "Wine Cellar": 0.08,
        "Home Theater": 0.07,
        "Custom Lighting": 0.05,
        "Vaulted Ceilings": 0.04,
        "Walk-in Closets": 0.03
    },
    "Kitchen/Bath": {
        "Quartz Countertops": 0.04,
        "Marble Countertops": 0.06,
        "Butler's Pantry": 0.05,
        "Double Islands": 0.06,
        "Custom Cabinetry": 0.07,
        "Luxury Appliances": 0.08
    },
    "Amenities": {
        "Gym": 0.06,
        "Sauna": 0.05,
        "Library": 0.04,
        "Home Office": 0.03,
        "Guest House": 0.10,
        "Security System": 0.03,
        "Outdoor Fireplaces": 0.04,
        "Balcony/Deck": 0.03,
        "Solar Panels": 0.05
    },
    "Architects": {
        "Garrett Nelson Studio": 0.07,
        "Presley Dixon": 0.06,
        "Other Custom Architect": 0.05
    }
}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "options": OPTIONS})

@app.post("/estimate", response_class=HTMLResponse)
async def estimate(request: Request):
    form = await request.form()
    sqft = float(form.get("sqft", 2500))
    selected_options = form.getlist("options")
    
    price = BASE_PRICE * sqft
    for category in OPTIONS:
        for option in OPTIONS[category]:
            if option in selected_options:
                price += price * OPTIONS[category][option]

    return templates.TemplateResponse("index.html", {
        "request": request,
        "options": OPTIONS,
        "estimate": f"${price:,.0f}"
    })

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
