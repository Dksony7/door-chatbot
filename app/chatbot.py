import g4f
import requests

def get_chatbot_response(user_input):
    """Generate a chatbot response using g4f and handle inventory-related queries."""
    try:
        # Check if the input matches a door size query
        if "×" in user_input:  # Assuming sizes like "32×80" are used
            # Use Render-hosted API URL
            api_url = "https://door-chatbot9oloollloololiiiool-ill.onrender.com/check_stock"
            response = requests.post(api_url, json={"size": user_input})
            
            if response.status_code == 200:
                data = response.json()
                if "stock" in data:
                    stock = data["stock"]
                    return f"The stock for size {user_input} is {stock}."
                elif "message" in data:
                    return data["message"]
            else:
                return f"Failed to fetch stock information. API response: {response.status_code}"
        
        # For general chat queries,
