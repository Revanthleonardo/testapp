# main.py

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pymongo import MongoClient

app = FastAPI()

# Connect to MongoDB
client = MongoClient("mongodb://mongo:27017/")
db = client["mydatabase"]
collection = db["mycollection"]

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI and MongoDB!"}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    item = collection.find_one({"item_id": item_id})
    if item:
        return item
    else:
        return JSONResponse(content={"error": "Item not found"}, status_code=404)