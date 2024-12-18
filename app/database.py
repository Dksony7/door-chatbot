from pymongo import MongoClient

# MongoDB Atlas connection
try:
    client = MongoClient("mongodb+srv://Dipika:9812009386@cluster0.dajxp.mongodb.net/?retryWrites=true&w=majority")
    db = client['doors']
    collection = db['doors']  # Global declaration of collection
    print("Application startup complete.")
except Exception as e:
    print("Failed to connect to MongoDB:", e)

# Function to fetch stock
def fetch_stock():
    try:
        stock_data = collection.find()
        for door in stock_data:
            print(f"Type: {door['type']}, Size: {door['size']}, Design: {door['design']}, Stock: {door['stock']}, Path: {door['image_path']}")
    except Exception as e:
        print("Error in fetching stock:", e)

# Call the function
fetch_stock()
