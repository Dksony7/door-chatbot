import requests
from typing import Dict
import g4f


def get_chatbot_response(user_input: str) -> str:
    """Generate a chatbot response using g4f and handle inventory-related queries."""
    try:
        # Check if the input matches a door size query (e.g., "32×80")
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
            else:
                return "Unexpected response format from the inventory API."

        # For general chat queries, use g4f
        response = g4f.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        )
        return response["choices"][0]["message"]["content"]

    except Exception as e:
        return f"An unexpected error occurred: {e}"
