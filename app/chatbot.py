from g4f.client import Client
import requests

def make_api_request(url: str, data: dict):
    """
    Make a POST request to the API.
    """
    try:
        response = requests.post(url, json=data, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def get_chatbot_response(user_input: str):
    """
    Handle user queries and generate chatbot responses.
    """
    try:
        # Handle door size queries
        if "×" in user_input:
            api_url = "http://127.0.0.1:10000/doors/" + user_input
            response = make_api_request(api_url, {})
            if "details" in response:
                return response
            elif "message" in response:
                return response["message"]

        # General chatbot response using g4f
        client = Client()
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Adjust the model if necessary
            messages=[{"role": "user", "content": user_input}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"
