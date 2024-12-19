import requests
from app.database import db
from flask import Flask, request, jsonify

# Initialize the Flask app
app = Flask(__name__)

# Access the 'doors' collection
doors = db['doors']

# Base URL for static files
base_url = "https://door-chatbot9oloollloololiiiool-ill.onrender.com/static/"



GEMINI_API_KEY = "AIzaSyDMLpDZ_Z_pwih4EkWygLSLtdDjuYnb1xI"
GEMINI_API_URL = (
    f"https://generativelanguage.googleapis.com/v1beta/models/"
    f"gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
)


def get_door_info(query):
    """
    Fetch door details from the database based on the query.
    """
    door_type_keywords = ['membrane', 'digital', 'warranty']
    matched_doors = []

    for door in doors.find():  # Assuming this fetches all doors
        for keyword in door_type_keywords:
            if keyword in query.lower():
                matched_doors.append(door)

    return matched_doors


def generate_gemini_response(query):
    """
    Communicate with the Gemini API to generate a response.
    """
    headers = {"Content-Type": "application/json"}
    payload = {"prompt": query}  # Use "prompt" as expected by Gemini API

    try:
        response = requests.post(GEMINI_API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the API response
        data = response.json()
        return data.get("candidates", [{}])[0].get("output", "No response available.")
    except requests.exceptions.RequestException as e:
        # Log or return an error message
        return f"Error communicating with Gemini API: {e}"


@app.route("/chat", methods=["POST"])
def chat():
    """
    Handle incoming user queries.
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
                "image": base_url + door.get("image_path", "")  # Assuming you store image path
            })

        return jsonify({"door_info": door_details})

    # If the query is not about doors, get a response from Gemini
    gemini_response = generate_gemini_response(user_query)

    return jsonify({"response": gemini_response})


if __name__ == "__main__":
    app.run(debug=True)
    
