from pymongo import MongoClient
from config import MONGO_URI, MONGO_DBNAME, MONGO_ACCOUNTSCOLLECTION, MONGO_SPFYIDSCOLLECTION

# Connection to MongoDB
client = MongoClient(MONGO_URI, connect=False)
# Access Spfy's DB in MongoDB
db = client[MONGO_DBNAME]
# Access the collection of accounts information from Spfy's DB
collection_accounts = db[MONGO_ACCOUNTSCOLLECTION]
collection_spfyids = db[MONGO_SPFYIDSCOLLECTION]

# Note: though 'store' refers to Redux Store, we use the same
# key for spfyids.
def mongo_update(uid, json=[], key='store', collection=MONGO_ACCOUNTSCOLLECTION):
    '''By default, updates the 'store' document in the accounts collection.
    '''
    if collection == MONGO_ACCOUNTSCOLLECTION:
        collection_accounts.update_one({'_id':uid},{'$set':{key:json}},upsert=True)
    elif collection == MONGO_SPFYIDSCOLLECTION:
        collection_spfyids.update_one({'_id':uid},{'$set':{key:json}},upsert=True)

# Note: though 'store' refers to Redux Store, we use the same
# key for spfyids.
def mongo_find(uid, key='store', collection=MONGO_ACCOUNTSCOLLECTION):
    if collection == MONGO_ACCOUNTSCOLLECTION:
        doc = collection_accounts.find_one({'_id':uid})
    elif collection == MONGO_SPFYIDSCOLLECTION:
        doc = collection_spfyids.find_one({'_id':uid})
    return doc[key]
