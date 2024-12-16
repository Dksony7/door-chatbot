import requests

# Set Gemini API key
gemini_api_key = "AIzaSyDzsEkRWRHsxY08cBmExiYI2wxlMV-AGeQ"

# Function to fetch door details based on size
def get_door_details(size):
    try:
        response = requests.get(f"https://door-chatbot9oloollloololiiiool-ill.onrender.com/doors/{size}", timeout=10)
        
        # Check for successful response
        if response.status_code != 200:
            return f"Sorry, could not fetch the door details. HTTP {response.status_code}."

        data = response.json()
        
        if "details" not in data or not data["details"]:
            return f"Size {size} ke liye koi door available nahi hai."

        # Create message
        message = f"Size {size} ke available doors:\n"
        for door_type, designs in data["details"].items():
            message += f"\nType: {door_type.capitalize()}\n"
            for design in designs:
                message += (
                    f"- Design: {design['design']}, Stock: {design['stock']}\n"
                    f"Image: {design['image_path']}\n\n"
                )
        return message.strip()  # Remove any trailing whitespace

    except requests.exceptions.Timeout:
        return "Request timed out. Please try again later."
    except requests.exceptions.RequestException as e:
        return f"Error fetching door details: {e}"

# Main chatbot response function
def chatbot_response(user_query):
    try:
        # Check if the user query includes a size specification
        if "size" in user_query.lower():
            # Extract size (assuming it's the last word)
            words = user_query.split()
            size = words[-1].replace("×", "x")  # Format size correctly
            return get_door_details(size)

        # Generate a response using Gemini's API
        response = requests.post(
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent",
            headers={
                "Authorization": f"Bearer {gemini_api_key}",
                "Content-Type": "application/json"
            },
            json={
                "prompt": {
                    "messages": [
                        {"author": "system", "content": "You are a multilingual assistant. Answer in the language of the user."},
                        {"author": "user", "content": user_query},
                    ]
                },
                "temperature": 0.7,
                "candidate_count": 1
            },
            timeout=10
        )

        # Check if the response is successful
        if response.status_code != 200:
            return f"Error in generating response. HTTP {response.status_code}"

        data = response.json()
        return data["candidates"][0]["output"]  # Extracting the first response from the API

    except requests.exceptions.Timeout:
        return "Request to Gemini API timed out. Please try again."
    except requests.exceptions.RequestException as e:
        return f"Error in generating response:\n\n{e}"

# Example usage
if __name__ == "__main__":
    user_query = input("Aapka sawaal: ")
    print(chatbot_response(user_query))
