from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# MongoDB URI
uri = "mongodb+srv://Dipika:9812009386@cluster0.dajxp.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Specify the correct database name
db = client['doors']  # MongoDB dashboard ke hisaab se lowercase 'doors'

# Test the connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")
