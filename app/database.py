from pymongo import MongoClient

# MongoDB Atlas connection
client = MongoClient("mongodb+srv://Dipika:9812009386@cluster0.dajxp.mongodb.net/?retryWrites=true&w=majority")

# Access the database and collection
db = client['doors']  # Database name
collection = db['doors']  # Collection name

# Function to fetch all door data
def fetch_all_doors():
    try:
        # Query all documents in the collection
        all_doors = collection.find()
        
        # Print each document
        print("Available Door Data:\n")
        for door in all_doors:
            print(f"Type: {door.get('type')}")
            print(f"Design: {door.get('design')}")
            print(f"Size: {door.get('size')}")
            print(f"Stock: {door.get('stock')}")
            print(f"Image Path: {door.get('image_path')}")
            print("-" * 40)  # Separator for clarity

    except Exception as e:
        print(f"Error fetching door data: {e}")

# Execute the function
if __name__ == "__main__":
    fetch_all_doors()
