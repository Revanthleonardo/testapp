from fastapi import FastAPI, Depends, HTTPException
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

app = FastAPI()

# MongoDB connection details
mongo_uri = "mongodb://localhost:27017/"

# Dependency to establish MongoDB connection
def get_db():
    try:
        client = MongoClient(mongo_uri)
        # Return the database connection to be used in route handlers
        return client
    except ConnectionFailure as e:
        raise HTTPException(status_code=500, detail=f"Failed to connect to MongoDB: {e}")

# Example route to check MongoDB connection
@app.get("/check_mongodb_connection")
def check_mongodb_connection(db: MongoClient = Depends(get_db)):
    try:
        # Check if the connection is successful by listing the databases
        database_list = db.list_database_names()
        return {"message": "Connected to MongoDB", "databases": database_list}
    except ConnectionFailure as e:
        raise HTTPException(status_code=500, detail=f"Failed to list databases in MongoDB: {e}")