from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from app.database import db  # Import the MongoDB connection from database.py

# Create the FastAPI app instance
app = FastAPI()

# Mount static files directory to serve images and other static assets
app.mount("/static", StaticFiles(directory="static"), name="static")

router = APIRouter()

@router.get("/")
def root():
    """
    Default route to check if the server is running.
    """
    return {"message": "Welcome to the Doors API!"}

@router.get("/doors/{size}")
def get_doors_by_size(size: str):
    """
    Fetch doors data for a specific size.
    """
    # Query MongoDB for doors of the specified size
    doors = list(db["doors"].find({"size": size}))

    if not doors:
        raise HTTPException(status_code=404, detail=f"No doors available for size {size}.")

    grouped_data = {}
    for door in doors:
        if door["type"] not in grouped_data:
            grouped_data[door["type"]] = []
        grouped_data[door["type"]].append({
            "design": door["design"],
            "stock": door["stock"],
            "image_path": door["image_path"]
        })

    return {"size": size, "details": grouped_data}

@router.post("/update_stock")
def update_stock(design: str, size: str, sold: int):
    """
    Update the stock of a specific door design and size.
    """
    # Find the specific door document
    door = db["doors"].find_one({"design": design, "size": size})
    if not door:
        raise HTTPException(status_code=404, detail=f"No door found for design {design} and size {size}.")

    new_stock = door["stock"] - sold
    if new_stock < 0:
        raise HTTPException(status_code=400, detail="Insufficient stock.")

    # Update the stock in the database
    db["doors"].update_one({"_id": door["_id"]}, {"$set": {"stock": new_stock}})
    return {"message": "Stock updated successfully."}

# Include the router in the app
app.include_router(router)
