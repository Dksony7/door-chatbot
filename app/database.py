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
    return db.doors  # Specify your collection name here
