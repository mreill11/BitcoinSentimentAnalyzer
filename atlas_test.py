import pymongo
from pymongo import MongoClient
import urllib


web_client = MongoClient("mongodb+srv://db_admin:Edgew00d!@cluster0-b82dm.mongodb.net/tweetsdb")
db = web_client.tweetsdb
# web_client.dabase_names()
collection = db.sentiment_collection
# db.collection_names()
#cursor = collection.find_one()
# collection = db['sentiment_collection']
#
# cursor = collection.find({})
# for document in cursor:
#     print(document["btc_price"])
