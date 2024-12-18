from pymongo import MongoClient

# MongoDB Atlas connection
try:
    client = MongoClient("mongodb+srv://Dipika:9812009386@cluster0.dajxp.mongodb.net/?retryWrites=true&w=majority")
    db = client['doors']  # Database name
    collection = db['doors']  # Collection name

    # Fetch stock data
    stock_data = collection.find()
    for door in stock_data:
        print(f"Type: {door['type']}, Size: {door['size']}, Design: {door['design']}, Stock: {door['stock']}, Path: {door['image_path']}")
except Exception as e:
    print("Error in fetching stock:", e)
