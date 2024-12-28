from fastapi import FastAPI
from app.routes import router, static_files
import os
import uvicorn

app = FastAPI()

# Mount static files
app.mount("/static", static_files, name="static")

# Include router for API and template handling
app.include_router(router)

if __name__ == "__main__":
    # Get the port from the environment variable or default to 10000
    port = int(os.getenv("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
