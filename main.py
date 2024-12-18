import os
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from app.routes import router
from app.chatbot import generate_gemini_response
    
# Initialize FastAPI app
app = FastAPI()

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include additional routes
app.include_router(router)

# Serve the index.html file
@app.get("/", response_class=HTMLResponse)
async def serve_index():
    try:
        with open("templates/index.html", "r") as file:
            return HTMLResponse(content=file.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Index file not found</h1>", status_code=404)

# Chatbot endpoint for POST requests
@app.post("/chat")
async def chat_with_bot(user_query: str = Form(...)):
    response = generate_gemini_response(user_query)  # Removed `await` if chatbot_response is not async
    return {"response": response}

# Optional: Allow GET requests for /chat
@app.get("/chat")
async def chat_with_bot_get(user_query: str):
    response = generate_gemini_response(user_query)  # Removed `await` if chatbot_response is not async
    return {"response": response}

# Run the app
if __name__ == "__main__":
    import uvicorn
    # Use environment variable for PORT or default to 8000
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
