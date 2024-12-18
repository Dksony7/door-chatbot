from pymongo import MongoClient

# MongoDB Atlas connection
client = MongoClient("mongodb+srv://Dipika:9812009386@cluster0.dajxp.mongodb.net/?retryWrites=true&w=majority")
db = client['doors']  # Database name: doors
collection = db['doors']  # Collection name: doors

# Function to fetch all door designs
def doors():
    try:
        # Query all documents in the collection
        all_doors = collection.find()
        
        # Display the data
        for door in all_doors:
            print(f"Design: {door.get('design')}")
            print(f"Image Path: {door.get('image_path')}")
            print(f"Size: {door.get('size')}")
            print("-" * 30)  # Separator for clarity

    except Exception as e:
        print(f"Error fetching data: {e}")

# Call the function
if __name__ == "__main__":
    fetch_all_doors()
