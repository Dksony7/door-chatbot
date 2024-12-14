import openai
import requests

# Your OpenAI API key
openai.api_key = "wBjYlt1APOeDrYcIQyNjrTAV"

# Function to get door details for a specific size
def get_door_details(size):
    # Make sure to replace with your Render API URL
    response = requests.get(f"https://your-render-url/doors/{size}")
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

# Function to handle chatbot response
def chatbot_response(user_query):
    if "size" in user_query.lower():
        size = user_query.split()[-1]
        return get_door_details(size)

    # OpenAI response generation
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a multilingual assistant. Answer in the language of the user."},
            {"role": "user", "content": user_query}
        ]
    )
    return response.choices[0].message["content"]
