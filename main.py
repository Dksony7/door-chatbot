from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from app.routes import router
import uvicorn
import os
from app.chatbot import chatbot_response  # Importing the chatbot functionality

app = FastAPI()

# Mounting the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include the router for the API routes
app.include_router(router)

# Root route serving the HTML page (chatbot interface)
@app.get("/", response_class=HTMLResponse)
async def read_root():
    # Serve the index.html file from the templates folder
    with open(os.path.join(os.path.dirname(__file__), "templates", "index.html")) as f:
        return f.read()

# Route to handle chatbot functionality (chat endpoint)
@app.get("/chat")
async def chat(user_query: str):
    # Call chatbot_response to get a reply
    response = chatbot_response(user_query)
    return {"response": response}

# Run the server (optional, you can run using 'uvicorn main:app --reload')
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
