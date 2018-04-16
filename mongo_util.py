import pymongo
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['tweetsdb']
collection = db['sentiment_collection']
cursor = collection.find({})
total = 0
count = 0
for document in cursor:
    total = total + document['sentiment']
    count = count + 1

avg = total / float(count)
print(avg)
print(count)
