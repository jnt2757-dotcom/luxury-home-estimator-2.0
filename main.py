from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

app = FastAPI(title="Thompson CBG Luxury Home Estimator")

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "frontend"))

# Mount static folder only if it exists
static_folder = BASE_DIR / "frontend" / "static"
if static_folder.exists():
    app.mount("/static", StaticFiles(directory=str(static_folder)), name="static")

# Estimator data
NEIGHBORHOODS = {"Eastover": 650, "Myers Park": 700, "Foxcroft": 675}
ARCHITECTS = {"Garrett Nelson Studio": 1.05, "Presley Dixon": 1.1, "Default": 1.0}
FEATURES = {
    "Pool": 1.15,
    "Slate Roof": 1.10,
    "Wood Roof": 1.05,
    "Marble Finishes": 1.20,
    "Smart Home Integration": 1.08,
    "Home Theater": 1.12,
    "Wine Cellar": 1.10,
    "Custom Landscaping": 1.07
}

@app.get("/", response_class=HTMLResponse)
def read_index(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "neighborhoods": NEIGHBORHOODS.keys(),
        "architects": ARCHITECTS.keys(),
        "features": FEATURES.keys()
    })

@app.post("/estimate", response_class=HTMLResponse)
def calculate_estimate(
    request: Request,
    neighborhood: str = Form(...),
    architect: str = Form(...),
    square_feet: float = Form(...),
    selected_features: list[str] = Form([])
):
    base_price = NEIGHBORHOODS.get(neighborhood, 650)
    architect_multiplier = ARCHITECTS.get(architect, 1.0)
    feature_multiplier = 1.0
    for feature in selected_features:
        feature_multiplier *= FEATURES.get(feature, 1.0)
    estimated_price = round(square_feet * base_price * architect_multiplier * feature_multiplier, 2)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "neighborhood": neighborhood,
        "architect": architect,
        "square_feet": square_feet,
        "features": selected_features,
        "estimated_price": f"${estimated_price:,.2f}",
        "neighborhoods": NEIGHBORHOODS.keys(),
        "architects": ARCHITECTS.keys(),
        "all_features": FEATURES.keys()
    })
