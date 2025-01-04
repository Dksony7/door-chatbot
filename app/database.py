from pymongo import MongoClient

# Connect to MongoDB Atlas
try:
    # Replace hardcoded credentials with environment variables for security in production
    client = MongoClient("mongodb+srv://Dipika:9812009386@cluster0.dajxp.mongodb.net/?retryWrites=true&w=majority")
    db = client["doors"]  # Database name
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
        inventory = list(inventory_collection.find({}, {"_id": 0}))  # Exclude the MongoDB _id field
        return inventory
    except Exception as e:
        print("Error fetching inventory: ", str(e))
        return []


def update_stock(design: str, size: str):
    """
    Reduce stock for a given design and size.
    Args:
        design (str): The design of the door (e.g., membrane, digital).
        size (str): The size of the door (e.g., 32×80).
    Returns:
        dict: Updated document or None if update fails.
    """
    try:
        result = inventory_collection.find_one_and_update(
            {"design": design, "size": size, "stock": {"$gt": 0}},  # Ensure stock > 0
            {"$inc": {"stock": -1}},  # Decrease stock by 1
            return_document=True  # Return the updated document
        )
        if result:
            print(f"Stock updated for {design} {size}: {result['stock']} remaining.")
        else:
            print(f"No stock available for {design} {size}.")
        return result
    except Exception as e:
        print("Error updating stock: ", str(e))
        return None


def get_stock_by_design_and_size(design: str, size: str):
    """
    Fetch stock for a specific design and size.
    Args:
        design (str): The design of the door.
        size (str): The size of the door.
    Returns:
        dict: The stock item with stock and image path, or None if not found.
    """
    try:
        stock_item = inventory_collection.find_one(
            {"design": design, "size": size},
            {"_id": 0, "stock": 1, "image_path": 1}  # Only return stock and image path
        )
        return stock_item
    except Exception as e:
        print(f"Error fetching stock for {design} and {size}: ", str(e))
        return None


def add_new_inventory_item(design: str, size: str, stock: int, image_path: str):
    """
    Add a new inventory item to the database.
    Args:
        design (str): The design of the door.
        size (str): The size of the door.
        stock (int): Initial stock quantity.
        image_path (str): Path to the door's image.
    Returns:
        dict: Inserted document details.
    """
    try:
        new_item = {
            "type": type 
            "design": design,
            "size": size,
            "stock": stock,
            "image_path": image_path
        }
        result = inventory_collection.insert_one(new_item)
        print(f"New inventory item added: {result.inserted_id}")
        return result
    except Exception as e:
        print("Error adding new inventory item: ", str(e))
        return None
