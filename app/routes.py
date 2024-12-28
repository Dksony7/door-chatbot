from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.chatbot import handle_message  # Import the chatbot handler
from app.database import db
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
    try:
        data = await request.json()
        message = data.get("message")
        if not message:
            raise HTTPException(status_code=400, detail="Message is required")

        # Call your chatbot handler function
        response = handle_message(message)  

        return {"reply": response}
    except Exception as e:
        # Log the error (recommended to use a proper logger)
        print(f"Error in /chat endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
        





    # Placeholder response logic
    response = {"reply": f"Received message: {message}"}
    return response
