import os
import zipfile

# Folder and file structure
base = "luxury-home-estimator-2.0"
frontend = os.path.join(base, "frontend")
os.makedirs(frontend, exist_ok=True)

with open(os.path.join(base, "main.py"), "w") as f:
    f.write("""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Luxury Home Cost Estimator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Project(BaseModel):
    gross_area: float
    floors: int
    finish_level: int
    foundation: str
    has_pool: int
    has_elevator: int
    site_difficulty: int
    location_index: float
    year: int

def dummy_estimate(project: Project):
    base = project.gross_area * 2500 * project.finish_level
    difficulty_factor = 1 + 0.05 * project.site_difficulty
    pool_factor = 1.2 if project.has_pool else 1.0
    elevator_factor = 1.15 if project.has_elevator else 1.0
    foundation_factor = 1.1 if project.foundation.lower() == "basement" else 1.0
    location_factor = project.location_index

    p50 = base * difficulty_factor * pool_factor * elevator_factor * foundation_factor * location_factor
    p10 = p50 * 0.9
    p90 = p50 * 1.1

    breakdown = {
        "Substructure/Foundation": p50 * 0.12,
        "Superstructure": p50 * 0.25,
        "Roofing": p50 * 0.08,
        "Finishes": p50 * 0.30,
        "MEP": p50 * 0.15,
        "Exterior/Landscape": p50 * 0.10
    }

    return {"p10": round(p10,0), "p50": round(p50,0), "p90": round(p90,0), "breakdown": breakdown}

@app.post("/estimate")
def estimate(project: Project):
    return dummy_estimate(project)
""")

with open(os.path.join(base, "requirements.txt"), "w") as f:
    f.write("fastapi\nuvicorn\npydantic\n")

with open(os.path.join(base, "README.md"), "w") as f:
    f.write("""
# Luxury Home Cost Estimator 2.0

Estimate luxury home construction costs with FastAPI and a simple HTML frontend.

## Features

- **Backend:** FastAPI (Python)
- **Frontend:** HTML/JS (`frontend/index.html`)
- **Estimate:** Inputs for area, floors, finish level, foundation, pool, elevator, site difficulty, location index, and year.
- **Outputs:** P10/P50/P90 cost estimates and a breakdown.

## Folder Structure
