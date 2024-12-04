from fastapi import FastAPI
from app.routes import router
import uvicorn

app = FastAPI()

# Include routes
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
