from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
import requests
from typing import Dict

router = APIRouter()

# Define a Pydantic model for the request body
class ChatRequest(BaseModel):
    message: str

def make_api_request(url: str, data: Dict) -> Dict:
    """
    Make a POST request to the external API and handle errors.
    """
    try:
        response = requests.post(url, json=data, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

@router.post("/chat")
async def chat(request: ChatRequest):
    """
    Handle chat requests and process both general chat and inventory queries.
    """
    user_input = request.message

    # Check if input is related to a door size (e.g., "32×80")
    if "×" in user_input:
        api_url = "https://door-chatbot9oloollloololiiiool-ill.onrender.com/check_stock"
        response = make_api_request(api_url, {"size": user_input})

        # Handle the stock response
        if "stock" in response:
            stock = response["stock"]
            return {"reply": f"The stock for size {user_input} is {stock}."}
        elif "message" in response:
            return {"reply": response["message"]}
        elif "error" in response:
            return {"reply": f"Error: {response['error']}"}

    # For general queries, fallback to g4f or other chatbot logic
    try:
        import g4f  # Ensure g4f is properly installed
        response = g4f.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        )
        chatbot_reply = response["choices"][0]["message"]["content"]
        return {"reply": chatbot_reply}
    except Exception as e:
        return {"reply": f"Error with chatbot: {str(e)}"}
