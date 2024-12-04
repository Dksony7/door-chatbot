from pymongo import MongoClient
import os

# Retrieve MongoDB URI from environment variable
uri = os.getenv("MONGO_URI")  # or hard-code the URI for testing

# Initialize MongoDB client
client = MongoClient(uri)

# Connect to the specific database
db = client.door_inventory  # Ensure 'db' is correctly defined and accessible

# Optionally, check the connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print("Error:", e)
