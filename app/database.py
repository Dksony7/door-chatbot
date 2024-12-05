from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# MongoDB URI
uri = "mongodb+srv://<db_username>:<db_password>@cluster0.dajxp.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Specify the database name
db = client['Door']  # Replace 'door_inventory' with your database name

# Test the connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")
