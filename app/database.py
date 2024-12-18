from pymongo import MongoClient

# MongoDB Atlas connection
client = MongoClient("mongodb+srv://Dipika:9812009386@cluster0.dajxp.mongodb.net/?retryWrites=true&w=majority")
db = client.doors  # Specify your database name

# Check connection
if db is not None:
    print("Connected to MongoDB Atlas.")
else:
    print("Failed to connect to MongoDB.")

def get_collection():
    # Return the MongoDB collection you want to use
    return db["doors"]  # Specify your collection name here

# Fetch stock example
try:
    collection = get_collection()  # Assign collection to a variable
    stock_data = collection.find_one({"design": "Digital"})  # Example query
    if stock_data:
        print("Stock Data:", stock_data)
    else:
        print("No stock found for the specified query.")
except Exception as e:
    print(f"Error in fetching stock: {e}")
