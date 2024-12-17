import requests

# Your actual API key from GCP Console
gemini_api_key = "AIzaSyDgnox9EPhJFq-vkC87yww9mC6q8bN8ta8"  # Replace with your actual key

# Function to call Gemini API
async def chatbot_response(user_query):
    try:
        # Request body for Gemini API
        request_body = {
            "contents": [
                {"role": "user", "parts": [{"text": user_query}]}
            ]
        }

        # Correct Gemini API Endpoint
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={gemini_api_key}"

        # Call the Gemini API
        response = requests.post(
            url,
            headers={
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
        return data["candidates"][0]["content"]["parts"][0]["text"]  # Extract the chatbot response

    except requests.exceptions.Timeout:
        return "Request to Gemini API timed out. Please try again."
    except requests.exceptions.RequestException as e:
        return f"Error in generating response: {e}"

# Example usage
import asyncio
response = asyncio.run(chatbot_response("What is the stock for 32×80 doors?"))
print(response)
