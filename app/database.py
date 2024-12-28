from pymongo import MongoClient

# MongoDB Atlas connection details
try:
    client = MongoClient("mongodb+srv://Dipika:9812009386@cluster0.dajxp.mongodb.net/?retryWrites=true&w=majority")
    db = client["doors"]  # Use your database name
    inventory_collection = db["doors"]  # Collection for inventory
    print("Connected to MongoDB Atlas.")
except Exception as e:
    print("Failed to connect to MongoDB: ", str(e))

def get_inventory():
    """
    Fetch the entire inventory from MongoDB.
    Returns a list of all inventory items.
    """
    try:
        inventory = list(inventory_collection.find({}, {"_id": 0}))
        return inventory
    except Exception as e:
        print("Error fetching inventory: ", str(e))
        return []

def update_stock(design, size):
    """
    Reduce stock for a given design and size.
    Updates the stock count in the database.
    Args:
        design (str): The design of the door (e.g., membrane, digital).
        size (str): The size of the door (e.g., 32x80).
    Returns:
        dict: Updated document or None if the update fails.
    """
    try:
        result = inventory_collection.find_one_and_update(
            {"design": design, f"sizes.{size}": {"$gt": 0}},
            {"$inc": {f"sizes.{size}": -1}},
            return_document=True
        )
        return result
    except Exception as e:
        print("Error updating stock: ", str(e))
        return None
