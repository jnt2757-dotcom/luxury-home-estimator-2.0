from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Neighborhoods
neighborhoods = [
    {"name": "Eastover", "builder": "Thompson Custom Building Group"},
    {"name": "Foxcroft", "builder": "Thompson Custom Building Group"},
    {"name": "Myers Park", "builder": "Thompson Custom Building Group"}
]

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "neighborhoods": neighborhoods})

@app.post("/estimate", response_class=HTMLResponse)
async def estimate(
    request: Request,
    sqft: int = Form(...),
    bedrooms: int = Form(...),
    bathrooms: int = Form(...),
    garage: int = Form(...),
    pool: str = Form(...),
    kitchen: str = Form(...),
    flooring: str = Form(...)
):
    # Basic luxury cost formula
    base_cost_per_sqft = 600
    bedroom_cost = 15000
    bathroom_cost = 10000
    garage_cost = 8000 * garage
    pool_cost = 100000 if pool == "Yes" else 0
    kitchen_cost = 40000 if kitchen == "Premium" else 0
    flooring_cost = 25000 if flooring == "Hardwood" else 0

    total_estimate = (
        sqft * base_cost_per_sqft
        + bedrooms * bedroom_cost
        + bathrooms * bathroom_cost
        + garage_cost
        + pool_cost
        + kitchen_cost
        + flooring_cost
    )

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "estimate": f"${total_estimate:,}",
            "neighborhoods": neighborhoods
        }
    )

