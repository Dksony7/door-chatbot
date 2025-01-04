from fastapi import APIRouter, HTTPException
from app.database import db

router = APIRouter()

@router.get("/doors/{size}")
async def get_doors_by_size(size: str):
    """
    Get all doors available for a specific size, grouped by type.
    """
    doors = list(db.doors.find({"size": size}))
    if not doors:
        return {"message": f"No doors available for size {size}."}

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
async def update_stock(design: str, size: str, sold: int):
    """
    Update the stock of a specific door design and size.
    """
    door = db.doors.find_one({"design": design, "size": size})
    if not door:
        raise HTTPException(status_code=404, detail=f"No door found for design {design} and size {size}.")
    
    new_stock = door["stock"] - sold
    if new_stock < 0:
        return {"message": "Insufficient stock."}

    db.doors.update_one({"_id": door["_id"]}, {"$set": {"stock": new_stock}})
    return {"message": "Stock updated successfully."}
