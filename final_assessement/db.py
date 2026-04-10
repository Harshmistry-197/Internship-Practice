from pymongo import MongoClient
import os
from dotenv import load_dotenv
from langgraph.checkpoint.mongodb import MongoDBSaver
load_dotenv()
mongo_connection_string = os.getenv("MONGODB_CONNECTION_STRING")

def connect():
    try:
        client = MongoClient(mongo_connection_string)
        db = client["chatbot_db"]
        collection = db["memory"]
        memory = MongoDBSaver(client, collection=collection)

        return memory

    except Exception as e:
        print(e)