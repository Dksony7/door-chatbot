from pymongo import MongoClient

def get_database():
    """
    Create and return a new MongoDB client and database connection.
    This ensures fork-safety by initializing after the fork.
    """
    client = MongoClient("mongodb+srv://Dipika:9812009386@cluster0.dajxp.mongodb.net/?retryWrites=true&w=majority")
    return client["doors"]  # Return the database object
