from fastapi import APIRouter
from app.database import db

router = APIRouter()

@router.get("/doors/{size}")
def get_doors_by_size(size: str):
    try:
        # Fetch doors from Door.Ok collection
        doors = list(db["Door.Ok"].find({"size": size}, {"_id": 0}))  # Removing '_id' from response
        if not doors:
            return {"message": f"No doors available for size {size}."}

        # Group doors by type
        grouped_data = {}
        for door in doors:
            door_type = door["type"]
            if door_type not in grouped_data:
                grouped_data[door_type] = []
            grouped_data[door_type].append({
                "design": door["design"],
                "stock": door["stock"],
                "image_path": door["image_path"]
            })

        return {"size": size, "details": grouped_data}
    except Exception as e:
        return {"error": f"An error occurred while fetching doors: {str(e)}"}

@router.post("/update_stock")
def update_stock(design: str, size: str, sold: int):
    try:
        # Fetch door by design and size from Door.Ok collection
        door = db["Door.Ok"].find_one({"design": design, "size": size})
        if not door:
            return {"message": f"No door found for design {design} and size {size}."}

        # Check stock and update
        new_stock = door["stock"] - sold
        if new_stock < 0:
            return {"message": "Insufficient stock."}

        db["Door.Ok"].update_one({"_id": door["_id"]}, {"$set": {"stock": new_stock}})
        return {"message": "Stock updated successfully."}
    except Exception as e:
        return {"error": f"An error occurred while updating stock: {str(e)}"}
