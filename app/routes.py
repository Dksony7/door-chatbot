from fastapi import APIRouter, HTTPException
from app.database import db

router = APIRouter()

@router.get("/doors/{size}")
def get_doors_by_size(size: str):
    # Normalize the input size (replace lowercase 'x' with the multiplication symbol '×')
    normalized_size = size.replace("x", "×")
    
    # Query the database for doors with the given size
    doors = list(db.doors.find({"size": normalized_size}))
    
    if not doors:
        raise HTTPException(status_code=404, detail=f"No doors available for size {size}.")
    
    # Group data by door type
    grouped_data = {}
    for door in doors:
        if door["type"] not in grouped_data:
            grouped_data[door["type"]] = []
        grouped_data[door["type"]].append({
            "design": door.get("design", "N/A"),
            "stock": door.get("stock", 0),
            "image_path": door.get("image_path", "")
        })
    
    return {"size": size, "details": grouped_data}


@router.post("/update_stock")
def update_stock(design: str, size: str, sold: int):
    # Normalize the input size
    normalized_size = size.replace("x", "×")
    
    # Find the door entry in the database
    door = db.doors.find_one({"design": design, "size": normalized_size})
    
    if not door:
        raise HTTPException(status_code=404, detail=f"No door found for design {design} and size {size}.")
    
    # Calculate the new stock
    new_stock = door["stock"] - sold
    if new_stock < 0:
        raise HTTPException(status_code=400, detail="Insufficient stock.")
    
    # Update the stock in the database
    db.doors.update_one({"_id": door["_id"]}, {"$set": {"stock": new_stock}})
    
    return {"message": "Stock updated successfully."}
