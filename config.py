import os

from dotenv import load_dotenv

from pymongo import MongoClient

from openai import OpenAI

load_dotenv()

def get_mongo_client():
    client = MongoClient(os.getenv('MONGODB_CONNECTION_STRING'))
    return client

def get_mongo_db():
    client = get_mongo_client()
    db = client.mineralsbook
    return db

def get_mongo_collection(name):
    db = get_mongo_db()
    collection = db[name]
    return collection

def get_openai_client():
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    return client
