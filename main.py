from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import router, static_files
import os
import uvicorn

app = FastAPI()

# Mount static files to serve images and other assets
app.mount("/static", static_files, name="static")

# Include the router from routes.py
app.include_router(router)

if __name__ == "__main__":
    # Get the port from the environment variable (Render sets PORT)
    port = int(os.getenv("PORT", 10000))  # Default to 10000 for Render

    # Run the app using uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)
