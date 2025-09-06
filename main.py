from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# Ensure frontend folder exists
if not os.path.isdir("frontend"):
    raise Exception("frontend folder not found in project root")

# Serve static files at /static
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Serve index.html at root URL
@app.get("/")
async def root():
    return FileResponse("frontend/index.html")
