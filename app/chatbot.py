import openai
import requests

# Set your OpenAI API key here
openai.api_key = "wBjYlt1APOeDrYcIQyNjrTAV"

# Update the URL to use the production URL (e.g., Render or Heroku URL)
# In your case, you may have a URL like "https://door-chatbot9oloollloololiiiool-ill.onrender.com"
DOOR_API_BASE_URL = "https://door-chatbot9oloollloololiiiool-ill.onrender.com/doors"  # Change to the deployed API URL

def get_door_details(size):
    # Send a GET request to the updated door details URL
    response = requests.get(f"{DOOR_API_BASE_URL}/{size}")
    if response.status_code != 200:
        return "Sorry, could not fetch the door details."

    data = response.json()
    if "details" not in data:
        return f"Size {size} ke liye koi door available nahi hai."

    message = f"Size {size} ke available doors:\n"
    for door_type, designs in data["details"].items():
        message += f"\nType: {door_type.capitalize()}\n"
        for design in designs:
            message += (
                f"- Design: {design['design']}, Stock: {design['stock']}\n"
                f"Image: {design['image_path']}\n\n"
            )
    return message

def chatbot_response(user_query):
    # Check if user is asking for door details (size)
    if "size" in user_query.lower():
        size = user_query.split()[-1]
        return get_door_details(size)

    # If user is asking for general queries, use OpenAI's GPT-4 model to generate a response
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a multilingual assistant. Answer in the language of the user."},
            {"role": "user", "content": user_query}
        ]
    )
    return response.choices[0].message["content"]
