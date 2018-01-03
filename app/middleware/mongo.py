from pymongo import MongoClient
from config import MONGO_URI, MONGO_DBNAME, MONGO_ACCOUNTSCOLLECTION

# Connection to MongoDB
client = MongoClient(MONGO_URI)
# Access Spfy's DB in MongoDB
db = client[MONGO_DBNAME]
# Access the collection of accounts information from Spfy's DB
collection_accounts = db[MONGO_ACCOUNTSCOLLECTION]

def mongo_update(uid, json, key='store'):
    '''By default, updates the 'store' document in the accounts collection.
    '''
    collection_accounts.update_one({'_id':uid},{'$set':{key:json}},upsert=True)

def mongo_find(uid, key='store'):
    doc = collection_accounts.find_ome({'_id':uid})
    return doc[key]
