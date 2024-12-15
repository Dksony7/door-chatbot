from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from app.routes import router
from app.chatbot import chatbot_response

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(router)

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    with open("templates/index.html") as file:
        return HTMLResponse(content=file.read())

@app.post("/chat")
async def chat_with_bot(request: Request):
    data = await request.form()
    user_query = data.get("user_query", "")
    response = chatbot_response(user_query)
    return {"response": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
