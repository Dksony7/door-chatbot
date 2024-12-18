from pymongo import MongoClient

# MongoDB Atlas connection
try:
    client = MongoClient("mongodb+srv://Dipika:9812009386@cluster0.dajxp.mongodb.net/?retryWrites=true&w=majority")
    db = client.doors
    # Test the connection by listing collections
    collections = db.list_collection_names()
    print("Connected to MongoDB Atlas. Collections:", collections)
except Exception as e:
    print("Failed to connect to MongoDB:", e)
