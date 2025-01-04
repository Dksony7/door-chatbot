from g4f.client import Client
import requests
from typing import Dict

def make_api_request(url: str, data: Dict) -> Dict:
    """
    Make a POST request to the API and handle errors gracefully.
    """
    try:
        response = requests.post(url, json=data, timeout=5)
        response.raise_for_status()  # Ensure status code is 200-299
        return response.json()  # Return JSON response from the API
    except requests.exceptions.Timeout:
        return {"error": "The request timed out. Please try again later."}
    except requests.exceptions.ConnectionError:
        return {"error": "Failed to connect to the server. Please check your network or try again later."}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def get_chatbot_response(user_input: str) -> str:
    """
    Generate a chatbot response for door size queries and general chat.
    """
    try:
        # Check if the user is querying door size availability (using '×' as the separator in size queries)
        if "×" in user_input:
            api_url = "http://127.0.0.1:10000/check_stock"  # Replace with your production URL
            response = make_api_request(api_url, {"size": user_input})
            
            # Process the API response for stock check
            if "stock" in response:
                stock = response["stock"]
                return f"The stock for size {user_input} is {stock}."
            elif "message" in response:
                return response["message"]  # Handle case where stock is not available
            elif "error" in response:
                return f"Error checking stock: {response['error']}"  # Handle API request errors

        # Handle general chat queries using g4f
        try:
            client = Client()
            response = client.chat.completions.create(
                model="gpt-4o-mini",  # Use the appropriate model for g4f
                messages=[{"role": "user", "content": user_input}]
            )
            return response.choices[0].message.content  # Return the chatbot's reply

        except Exception as g4f_error:
            return f"Error generating a response: {g4f_error}"  # Handle errors with g4f

    except Exception as e:
        return f"An unexpected error occurred: {e}"  # General exception for unforeseen errors
