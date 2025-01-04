from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.chatbot import get_chatbot_response
from app.database import get_stock_by_design_and_size, get_inventory

router = APIRouter()

# Setup templates for rendering HTML pages
templates = Jinja2Templates(directory="templates")

# Serve static files (images, CSS, etc.)
static_files = StaticFiles(directory="static")

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """
    Render the homepage (index.html).
    """
    return templates.TemplateResponse("index.html", {"request": request})


@router.post("/chat")
async def chat(request: Request):
    """
    Handle chat messages by passing them to the chatbot handler.
    """
    try:
        data = await request.json()
        message = data.get("message")
        if not message:
            raise HTTPException(status_code=400, detail="Message is required")

        # Call chatbot handler function
        response = get_chatbot_response(message)
        return {"reply": response}

    except Exception as e:
        print(f"Error in /chat endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/check_stock")
async def check_stock(request: Request):
    """
    Check stock for a given door size.
    """
    try:
        data = await request.json()
        size = data.get("size")
        if not size:
            raise HTTPException(status_code=400, detail="Size is required")

        # Query the stock from the database
        stock_item = get_stock_by_design_and_size("digital", size)  # Replace "digital" if design varies
        if stock_item:
            stock = stock_item.get("stock", 0)
            return {"size": size, "stock": stock}
        else:
            return {"message": f"No stock found for size {size}."}

    except Exception as e:
        print(f"Error in /check_stock endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/inventory")
async def inventory():
    """
    Get the entire inventory.
    """
    try:
        inventory_data = get_inventory()
        return {"inventory": inventory_data}

    except Exception as e:
        print(f"Error in /inventory endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
