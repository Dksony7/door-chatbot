@router.get("/doors/{size}")
def get_doors_by_size(size: str):
    print(f"Finding doors with size: {size}")  # Log size
    doors = list(db.doors.find({"size": size}))
    print(f"Query Result: {doors}")  # Log MongoDB query result

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
