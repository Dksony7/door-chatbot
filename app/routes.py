from fastapi import FastAPI, APIRouter
from pymongo import MongoClient

app = FastAPI()
router = APIRouter()

# Global variable for MongoDB connection
db = None

@app.on_event("startup")
def startup_db_client():
    """
    Initialize MongoDB client and database connection when the server starts.
    """
    global db
    uri = "mongodb+srv://Dipika:9812009386@cluster0.dajxp.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri)
    db = client["doors"]  # Use the correct database name
    print("Connected to the MongoDB database!")


@app.on_event("shutdown")
def shutdown_db_client():
    """
    Close the MongoDB client connection when the server shuts down.
    """
    global db
    db = None
    print("MongoDB connection closed.")


@app.get("/")
def root():
    """
    Default route to check if the server is running.
    """
    return {"message": "Welcome to the Doors API!"}


@router.get("/doors/{size}")
def get_doors_by_size(size: str):
    """
    Fetch doors data for a specific size.
    """
    doors = list(db["doors"].find({"size": size}))  # Query MongoDB for the given size
    print(f"Query Results for size {size}: {doors}")  # Debugging: Log the query results

    if not doors:
        return {"message": f"No doors available for size {size}."}

    grouped_data = {}
    for door in doors:
        if door["type"] not in grouped_data:
            grouped_data[door["type"]] = []
        grouped_data[door["type"]].append({
            "design": door["design"],
            "stock": door["stock"],
            "image_path": door["image_path"]
        })

    return {"size": size, "details": grouped_data}


@router.post("/update_stock")
def update_stock(design: str, size: str, sold: int):
    """
    Update the stock of a specific door design and size.
    """
    door = db["doors"].find_one({"design": design, "size": size})
    if not door:
        return {"message": f"No door found for design {design} and size {size}."}

    new_stock = door["stock"] - sold
    if new_stock < 0:
        return {"message": "Insufficient stock."}

    db["doors"].update_one({"_id": door["_id"]}, {"$set": {"stock": new_stock}})
    return {"message": "Stock updated successfully."}


# Include the router
app.include_router(router)
