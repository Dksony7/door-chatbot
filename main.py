from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import router, static_files

app = FastAPI()

# Mount static files
app.mount("/static", static_files, name="static")

# Include the router
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
