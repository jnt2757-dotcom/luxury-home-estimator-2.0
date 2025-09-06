from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

app = FastAPI(title="Thompson CBG Luxury Home Estimator")

# Paths for templates and static files
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "frontend"))
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "frontend/static")), name="static")

# Example neighborhoods and average per square foot prices
NEIGHBORHOODS = {
    "Eastover": 650,
    "Myers Park": 700,
    "Foxcroft": 675
}

# Example architects with modifiers (prices vary based on architect)
ARCHITECTS = {
    "Garrett Nelson Studio": 1.05,
    "Presley Dixon": 1.1,
    "Default": 1.0
}

# Example features with price multipliers
FEATURES = {
    "Pool": 1.15,
    "Slate Roof": 1.10,
    "Wood Roof": 1.05,
    "Marble Finishes": 1.20,
    "Smart Home Integration": 1.08
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
    # Base price per square foot by neighborhood
    base_price = NEIGHBORHOODS.get(neighborhood, 650)

    # Architect multiplier
    architect_multiplier = ARCHITECTS.get(architect, 1.0)

    # Features multiplier
    feature_multiplier = 1.0
    for feature in selected_features:
        feature_multiplier *= FEATURES.get(feature, 1.0)

    # Final estimate
    estimated_price = square_feet * base_price * architect_multiplier * feature_multiplier
    estimated_price = round(estimated_price, 2)

    # Context to render results page
    context = {
        "request": request,
        "neighborhood": neighborhood,
        "architect": architect,
        "square_feet": square_feet,
        "features": selected_features,
        "estimated_price": f"${estimated_price:,.2f}"
    }

    return templates.TemplateResponse("index.html", context)

# Optional API endpoint for JSON estimates (for mobile or future integration)
@app.post("/api/estimate")
def api_estimate(
    neighborhood: str,
    architect: str,
    square_feet: float,
    features: list[str] = []
):
    base_price = NEIGHBORHOODS.get(neighborhood, 650)
    architect_multiplier = ARCHITECTS.get(architect, 1.0)
    feature_multiplier = 1.0
    for feature in features:
        feature_multiplier *= FEATURES.get(feature, 1.0)
    estimated_price = square_feet * base_price * architect_multiplier * feature_multiplier
    return {"estimated_price": round(estimated_price, 2)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
