# Luxury Home Cost Estimator 2.0

Estimate luxury home construction costs with FastAPI and a simple HTML frontend.

## Features

- **Backend:** FastAPI (Python)
- **Frontend:** HTML/JS (`frontend/index.html`)
- **Estimate:** Inputs for area, floors, finish level, foundation, pool, elevator, site difficulty, location index, and year.
- **Outputs:** P10/P50/P90 cost estimates and a breakdown.

## Folder Structure

```
luxury-home-estimator-2.0/
  main.py
  requirements.txt
  frontend/
    index.html
```

## How to Run Locally

1. Install dependencies:
    ```
    pip install -r requirements.txt
    ```
2. Start the backend:
    ```
    uvicorn main:app --reload
    ```
3. Open `frontend/index.html` in your browser.

## Deployment

- Deploy on [Render](https://render.com/) or [Railway](https://railway.app/)
- **Start command:**  
    ```
    uvicorn main:app --host 0.0.0.0 --port 8000
    ```
- For production, update the fetch URL in `index.html` to match your deployed backend.

## License

MIT