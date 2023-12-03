from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

app = FastAPI()

# MongoDB Connection
mongo_client = AsyncIOMotorClient("mongodb://localhost:27017")
database = mongo_client["testdb"]
collection = database["items"]


class Item(BaseModel):
    name: str
    description: str = None


@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    # Convert Pydantic model to a dictionary
    item_dict = item.dict()

    # Insert document into MongoDB
    result = await collection.insert_one(item_dict)
    item_id = str(result.inserted_id)

    # Return the created item with its new MongoDB ID
    return {**item.dict(), "id": item_id}


@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str):
    # Find document in MongoDB by ID
    result = await collection.find_one({"_id": ObjectId(item_id)})

    # If document is not found, raise HTTP 404 Not Found
    if result is None:
        raise HTTPException(status_code=404, detail="Item not found")

    # Convert MongoDB document to Pydantic model
    return {**result, "id": item_id}


@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    # Convert Pydantic model to a dictionary
    item_dict = item.dict()

    # Update document in MongoDB by ID
    result = await collection.update_one({"_id": ObjectId(item_id)}, {"$set": item_dict})

    # If document is not found, raise HTTP 404 Not Found
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")

    # Return the updated item
    return {**item.dict(), "id": item_id}


@app.delete("/items/{item_id}", response_model=dict)
async def delete_item(item_id: str):
    # Delete document in MongoDB by ID
    result = await collection.delete_one({"_id": ObjectId(item_id)})

    # If document is not found, raise HTTP 404 Not Found
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")

    # Return a response indicating the deletion
    return {"message": "Item deleted successfully"}
