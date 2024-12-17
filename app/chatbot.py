import requests

# Your actual API key from GCP Console
gemini_api_key = "AIzaSyDzsEkRWRHsxY08cBmExiYI2wxlMV-AGeQ"  # Replace with your actual key

# Function to call Gemini API
async def chatbot_response(user_query):
    try:
        # Request body for Gemini API
        request_body = {
            "prompt": {
                "messages": [
                    {"author": "system", "content": "You are a multilingual assistant. Answer in the language of the user."},
                    {"author": "user", "content": user_query},
                ]
            },
            "temperature": 0.7,
            "candidate_count": 1
        }

        # Call the Gemini API
        response = requests.post(
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent",
            headers={
                "Authorization": f"Bearer {gemini_api_key}",
                "Content-Type": "application/json",
            },
            json=request_body,
            timeout=10
        )

        # Check for successful response
        if response.status_code != 200:
            return f"Error in generating response. HTTP {response.status_code}: {response.text}"

        # Parse the response
        data = response.json()
        return data["candidates"][0]["output"]  # Extract the chatbot response

    except requests.exceptions.Timeout:
        return "Request to Gemini API timed out. Please try again."
    except requests.exceptions.RequestException as e:
        return f"Error in generating response: {e}"
        
