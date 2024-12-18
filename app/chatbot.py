
import requests
from app.database import db
import asyncio
from flask import Flask, request, jsonify

# Initialize the Flask app
app = Flask(__name__)

# Access the 'doors' collection
doors = db['doors']

# Gemini API key (already provided)
gemini_api_key = "AIzaSyDgnox9EPhJFq-vkC87yww9mC6q8bN8ta8"
base_url = "https://door-chatbot9oloollloololiiiool-ill.onrender.com/static/"


def get_door_info(query):
    """
    Function to process the query and fetch door details from the database.
    """
    # Check if the query mentions a door type
    door_type_keywords = ['membrane', 'digital', 'warranty']
    matched_doors = []

    for door in doors.find():  # Assuming this fetches all doors
        for keyword in door_type_keywords:
            if keyword in query.lower():
                matched_doors.append(door)

    return matched_doors

def generate_gemini_response(query):
    """
    Function to communicate with the Gemini API to generate responses.
    """
    response = requests.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=AIzaSyDgnox9EPhJFq-vkC87yww9mC6q8bN8ta8",  # Replace with actual Gemini API URL
        headers={"Authorization": f"Bearer {gemini_api_key}"},
        json={"query": query}
    )
    return response.json().get('response', 'Sorry, I couldn\'t understand the query.')

@app.route("/chat", methods=["POST"])
def chat():
    """
    Endpoint to handle incoming user queries.
    """
    user_query = request.json.get("query")

    if not user_query:
        return jsonify({"error": "Query is required"}), 400

    # Fetch door information if related to doors
    door_info = get_door_info(user_query)

    if door_info:
        # Prepare door details to send as response
        door_details = []
        for door in door_info:
            door_details.append({
                "type": door.get("type"),
                "design": door.get("design"),
                "size": door.get("size"),
                "stock": door.get("stock"),
                "image": base_url + door.get("image_path")  # Assuming you store image path
            })

        return jsonify({"door_info": door_details})

    # If the query is not about doors, get a response from Gemini
    gemini_response = generate_gemini_response(user_query)

    return jsonify({"response": gemini_response})

if __name__ == "__main__":
    app.run(debug=True)
