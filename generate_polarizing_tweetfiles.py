from pymongo import MongoClient

client = MongoClient("mongodb+srv://db_admin:Edgew00d!@cluster0-b82dm.mongodb.net/tweetsdb")
db = client.tweetsdb
sentiment_collection = db.sentiment_collection
pos_tweets = open("very_pos_tweets.txt", 'w')
neg_tweets = open("very_neg_tweets.txt", 'w')

cursor = sentiment_collection.find({})
for document in cursor:
    if "tweet" in document:
        if document['sentiment'] > 0:
            pos_tweets.write(document['tweet'])
            pos_tweets.write("\n")
        else:
            neg_tweets.write(document['tweet'])
            neg_tweets.write("\n")
