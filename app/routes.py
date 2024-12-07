from fastapi import APIRouter
from app.database import db

# Initialize the router
router = APIRouter()

@router.get("/doors/{size}")
def get_doors_by_size(size: str):
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
def update_stock(design: str, size: str, sold: int):
    door = db.doors.find_one({"design": design, "size": size})
    if not door:
        return {"message": f"No door found for design {design} and size {size}."}
    
    new_stock = door["stock"] - sold
    if new_stock < 0:
        return {"message": "Insufficient stock."}

    db.doors.update_one({"_id": door["_id"]}, {"$set": {"stock": new_stock}})
    return {"message": "Stock updated successfully."}
