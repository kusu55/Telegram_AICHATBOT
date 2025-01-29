from pymongo import MongoClient
from config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client["telegram_ai"]
users_collection = db["users"]
chats_collection = db["chats"]
files_collection = db["files"]
referrals_collection = db["referrals"]
