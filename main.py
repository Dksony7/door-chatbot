from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import router, static_files
import os

app = FastAPI()

# Mount static files
app.mount("/static", static_files, name="static")

# Include the router
app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    # Get the port from an environment variable or use 8000 as default
    port = int(os.getenv("PORT", 8000))

    uvicorn.run(app, host="0.0.0.0", port=port)
