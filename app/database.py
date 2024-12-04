from pymongo import MongoClient

# MongoDB Atlas connection
client = MongoClient("mongodb+srv://dipika:9812009386@cluster0.dajxp.mongodb.net/?retryWrites=true&w=majority")
db = client.door_inventory

# Check connection
if db:
    print("Connected to MongoDB Atlas.")
else:
    print("Failed to connect to MongoDB.")
