import asyncio
from app.database import db  # Corrected import
doors = db['doors']  # 'doors' collection access karo
import requests
gemini_api_key = "AIzaSyDgnox9EPhJFq-vkC87yww9mC6q8bN8ta8"




# Assuming your images are hosted in a static folder structure (e.g., Render or GitHub Pages)
base_url = "https://door-chatbot9oloollloololiiiool-ill.onrender.com/static/"

async def chatbot_response(user_query):
    try:
        # Normalize the query and check for different types of requests
        if "stock" in user_query.lower():
            # Example: "32×80 stock" or "Membrane stock"
            return await get_stock(user_query)
        
        elif "update stock" in user_query.lower():
            # Example: "update stock 2 digital1 32×78"
            return await update_stock(user_query)
        
        else:
            return "Sorry, I didn't understand the request."

    except Exception as e:
        return f"Error: {str(e)}"

async def get_stock(user_query):
    try:
        # Extract size or design or type from the query
        if "digital" in user_query.lower():
            design = user_query.split(" ")[0]
            door_data = doors.find_one({"design": design})
        
        elif "membrane" in user_query.lower():
            door_data = doors.find_one({"type": "membrane"})
        
        elif "32×80" in user_query:
            door_data = doors.find_one({"size": "32×80"})
        
        if door_data:
            # Determine the appropriate image URL
            image_url = get_image_url(door_data)
            return f"Stock for {door_data['design']} {door_data['size']}: {door_data['stock']} doors. Image: {image_url}"
        else:
            return "No data found for the requested door."

    except Exception as e:
        return f"Error in fetching stock: {str(e)}"

async def update_stock(user_query):
    try:
        # Extract the details from the query (amount, design, size)
        parts = user_query.split()
        sold_quantity = int(parts[2])  # Example: 2
        design = parts[3]  # Example: "digital1"
        size = parts[4]  # Example: "32×78"
        
        # Find the door in the collection
        door_data = doors.find_one({"design": design, "size": size})
        
        if door_data:
            # Update the stock
            new_stock = door_data['stock'] - sold_quantity
            doors.update_one(
                {"design": design, "size": size},
                {"$set": {"stock": new_stock}}
            )
            # Get the updated image URL
            image_url = get_image_url(door_data)
            return f"Stock updated! Now {design} {size} has {new_stock} doors. Image: {image_url}"
        else:
            return "No data found for the specified door."
    
    except Exception as e:
        return f"Error in updating stock: {str(e)}"

def get_image_url(door_data):
    # Determine the folder based on the door type and design
    if door_data['type'] == "membrane":
        folder = "membrane"
    elif door_data['type'] == "digital":
        folder = "digital"
    elif door_data['type'] == "warranty":
        folder = "warranty"
    else:
        folder = "default"

    # Construct the image URL (assuming it's hosted on a public URL like GitHub Pages or Render)
    image_filename = f"{door_data['design']}.jpg"  # Assuming the design is used as the filename
    image_url = f"{base_url}{folder}/{image_filename}"
    
    return image_url

# Example Usage

response = asyncio.run(chatbot_response("update stock 2 digital1 32×78"))
print(response)

response = asyncio.run(chatbot_response("32×80 stock"))
print(response)



