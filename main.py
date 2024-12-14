from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from app.routes import router
import uvicorn
import os

app = FastAPI()

# Include routes
app.include_router(router)

# Serve static files (if needed)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def root():
    """
    Serve the index.html file for the chatbot frontend.
    """
    with open("templates/index.html") as file:
        return file.read()

if __name__ == "__main__":
    # Use the PORT environment variable if available, default to 8000
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
