from pymongo import MongoClient

# MongoDB Atlas connection details
try:
    # MongoDB connection URI with hardcoded credentials (use environment variables for production)
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
        # Fetching all items without the _id field
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
        # Querying by design and size to update stock
        result = inventory_collection.find_one_and_update(
            {"design": design, "size": size, "stock": {"$gt": 0}},  # Only update if stock > 0
            {"$inc": {"stock": -1}},  # Decrease the stock by 1
            return_document=True  # Return the updated document
        )
        return result
    except Exception as e:
        print("Error updating stock: ", str(e))
        return None

def get_stock_by_design_and_size(design, size):
    """
    Fetch stock for a given design and size.
    Args:
        design (str): The design of the door.
        size (str): The size of the door.
    Returns:
        dict: The stock item with stock and image path, or None if not found.
    """
    try:
        # Find the stock document based on design and size
        stock_item = inventory_collection.find_one({"design": design, "size": size}, {"_id": 0})
        if stock_item:
            return stock_item  # Return stock item with all fields (stock, image_path, etc.)
        return None  # Return None if no matching item found
    except Exception as e:
        print(f"Error fetching stock for {design} and {size}: ", str(e))
        return None
