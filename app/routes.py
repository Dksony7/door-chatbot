from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.chatbot import get_chatbot_response  # Import the chatbot handler
from app.database import db  # Assume this is your MongoDB connection

 router = APIRouter()

@router.post("/check_stock")
async def check_stock(request: Request):
    """
    Check stock availability for a given design and size.
    """
    try:
        data = await request.json()
        design = data.get("design")
        size = data.get("size")

        if not design or not size:
            raise HTTPException(status_code=400, detail="Design and size are required")

        # Query the inventory collection based on the "design" and "size"
        stock_item = inventory_collection.find_one({"design": design, "size": size}, {"_id": 0})

        if not stock_item:
            return {"status": "success", "stock": 0, "message": "Item not found."}  # Return 0 if no matching item is found

        # Fetch the stock count
        stock = stock_item["stock"]
        # Add the image path to the response
        image_path = stock_item["image_path"]

        return {"status": "success", "stock": stock, "image_path": image_path}  # Return stock count and image path

    except Exception as e:
        print(f"Error in /check_stock endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")       
