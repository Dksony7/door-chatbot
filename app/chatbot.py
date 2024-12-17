import asyncio
from app.database import get_collection  # Corrected import

gemini_api_key = "AIzaSyDgnox9EPhJFq-vkC87yww9mC6q8bN8ta8"

async def chatbot_response(door_size):
    try:
        # Fetch data from MongoDB
        collection = get_collection()  # Get the collection from database.py
        door_data = collection.find_one({"size": door_size})
        if not door_data:
            return f"No data found for size {door_size}."

        # Prepare user query
        user_query = f"What is the stock for {door_size} doors? Available stock is {door_data['stock']}."

        # Gemini API Request
        request_body = {
            "contents": [{"role": "user", "parts": [{"text": user_query}]}]
        }
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={gemini_api_key}"

        response = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            json=request_body,
            timeout=10
        )

        # Check for successful response
        if response.status_code != 200:
            return f"Error: HTTP {response.status_code}: {response.text}"

        # Parse the response
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]

    except Exception as e:
        return f"Error: {str(e)}"

async def chatbot_response(door_size):
    try:
        # Fetch data from MongoDB
        collection = get_collection()
        door_data = collection.find_one({"size": door_size})
        if not door_data:
            return f"No data found for size {door_size}."

        # Prepare user query and return more detailed response
        user_query = f"What is the stock for {door_size} doors? Available stock is {door_data['stock']}."
        stock_info = f"Stock for size {door_size}: {door_data['stock']} units available."
        other_details = f"Price: {door_data.get('price', 'N/A')}, Design: {door_data.get('design', 'N/A')}"

        # Combine and return a detailed response
        return f"{stock_info}\n{other_details}"

    except Exception as e:
        return f"Error: {str(e)}"
