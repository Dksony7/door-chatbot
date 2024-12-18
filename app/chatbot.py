from pymongo import MongoClient
import asyncio

# MongoDB Connection
client = MongoClient("mongodb+srv://Dipika:9812009386@cluster0.mongodb.net/?retryWrites=true&w=majority")
db = client['doors']  # Database name
doors = db['doors']  # Collection name

# Base URL for images
base_url = "https://door-chatbot9oloollloololiiiool-ill.onrender.com/static/"

async def chatbot_response(user_query):
    try:
        if "stock" in user_query.lower():
            return await get_stock(user_query)
        elif "update stock" in user_query.lower():
            return await update_stock(user_query)
        else:
            return "Sorry, I didn't understand the request."
    except Exception as e:
        return f"Error: {str(e)}"

async def get_stock(user_query):
    try:
        query = {}
        if "digital" in user_query.lower():
            query["type"] = "digital"
        elif "membrane" in user_query.lower():
            query["type"] = "membrane"
        elif "32×80" in user_query:
            query["size"] = "32×80"

        door_data = doors.find_one(query)

        if door_data:
            image_url = get_image_url(door_data)
            return f"Stock for {door_data['design']} {door_data['size']}: {door_data['stock']} doors. Image: {image_url}"
        else:
            return "No data found for the requested door."

    except Exception as e:
        return f"Error in fetching stock: {str(e)}"

async def update_stock(user_query):
    try:
        parts = user_query.split()
        sold_quantity = int(parts[2])
        design = parts[3]
        size = parts[4]

        door_data = doors.find_one({"design": design, "size": size})

        if door_data:
            new_stock = max(0, door_data['stock'] - sold_quantity)
            doors.update_one(
                {"design": design, "size": size},
                {"$set": {"stock": new_stock}}
            )
            image_url = get_image_url(door_data)
            return f"Stock updated! Now {design} {size} has {new_stock} doors. Image: {image_url}"
        else:
            return "No data found for the specified door."
    except Exception as e:
        return f"Error in updating stock: {str(e)}"

def get_image_url(door_data):
    folder = door_data['type']
    image_filename = f"{door_data['design']}.jpg"
    return f"{base_url}{folder}/{image_filename}"

# Example Usage
response = asyncio.run(chatbot_response("update stock 2 digital1 32×80"))
print(response)

response = asyncio.run(chatbot_response("32×80 stock"))
print(response)
