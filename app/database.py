from pymongo import MongoClient
import os

# Fetch MongoDB URI from environment variable
mongo_uri = os.environ.get("MONGO_URI", "mongodb+srv://<db_username>:<db_password>@cluster0.dajxp.mongodb.net/?retryWrites=true&w=majority")

# MongoDB Atlas connection
client = MongoClient(mongo_uri)

# Check connection by fetching database names
try:
    # This will raise an exception if the connection fails
    db = client.door_inventory
    client.server_info()  # Fetch server info to verify connection
    print("Connected to MongoDB Atlas successfully.")
except Exception as e:
    print(f"Failed to connect to MongoDB Atlas. Error: {e}")
