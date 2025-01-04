from fastapi import FastAPI
from app.routes import router
import uvicorn

app = FastAPI()

# Include the router for API routes
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)
