from fastapi import FastAPI
from app.routes import router
import uvicorn
import os

app = FastAPI()

# Include routes
app.include_router(router)

if __name__ == "__main__":
    # Use the PORT environment variable if available, default to 8000
    port = int(os.environ.get("PORT", 8000))

    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
