import g4f
import requests
from typing import Dict

def make_api_request(url: str, data: Dict) -> Dict:
    """Make a POST request to the API."""
    try:
        response = requests.post(url, json=data, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def get_chatbot_response(user_input: str) -> str:
    """Generate a chatbot response using g4f and handle inventory-related queries."""
    try:
        # Check if the input matches a door size query
        if "×" in user_input:  
            api_url = "https://door-chatbot9oloollloololiiiool-ill.onrender.com/check_stock"
            response = make_api_request(api_url, {"size": user_input})
            
            if "stock" in response:
                stock = response["stock"]
                return f"The stock for size {user_input} is {stock}."
            elif "message" in response:
                return response["message"]
            elif "error" in response:
                return response["error"]
        
        # For general chat queries, use g4f
        try:
            response = g4f.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": user_input}]
            )
            return response["choices"][0]["message"]["content"]
        except g4f.exceptions.APIError as e:
            return f"Error: {e}"

    except Exception as e:
        return f"Error: {e}"
