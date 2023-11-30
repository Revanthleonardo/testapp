from fastapi import FastAPI
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://rev:4qXHNy2rBXNwmTeq@cluster.kigfmdr.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# app = FastAPI()


# @app.get("/")
# def read_root():
#     return {"Hello": "World"}
    

# @app.get("/items/{item_id}")
# def read_item(item_id: str):
#     return {"item_id": item_id}


# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)