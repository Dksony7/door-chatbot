from pymongo import MongoClient

# MongoDB Atlas connection
client = MongoClient("mongodb+srv://Dipika:9812009386@cluster0.dajxp.mongodb.net/?retryWrites=true&w=majority")
db = client.doors

# Check connection
if db is not None:  # Change yahan kiya gaya hai
    print("Connected to MongoDB Atlas.")
else:
    print("Failed to connect to MongoDB.")
