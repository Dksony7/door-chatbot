from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from app.database import db  # Import the MongoDB connection from database.py

# Mount static files using the FastAPI instance in main.py
static_files = StaticFiles(directory="static")

# Create the APIRouter instance
router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def serve_index():
    """
    Serve the index.html file for the chatbot frontend.
    """
    with open("templates/index.html") as file:
        return file.read()

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
