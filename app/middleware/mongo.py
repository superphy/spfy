from pymongo import MongoClient
from config import MONGO_URI, MONGO_DBNAME, MONGO_ACCOUNTSCOLLECTION

# Connection to MongoDB
client = MongoClient(MONGO_URI)
# Access Spfy's DB in MongoDB
db = client[MONGO_DBNAME]
# Access the collection of accounts information from Spfy's DB
collection = db[MONGO_ACCOUNTSCOLLECTION]

def mongo_update(uid, json):
    try:
        collection.update_one({'_id':uid},{'$set':{'store':json}},{upsert:true})
        return True
    except:
        return False
