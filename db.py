from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["lost_found_db"]

users = db["users"]
items = db["items"]