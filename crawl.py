from __future__ import print_function
import tweepy
import json
from pymongo import MongoClient

class StreamListener(tweepy.StreamListener):
    """
    tweepy.StreamListener is a class provided by tweepy used to access
    the Twitter Streaming API. It allows us to retrieve tweets in real time.
    """
    def on_connect(self):
        """Called when the connection is made"""
        print("You're connected to the streaming server.")

    def on_error(self, status_code):
        """This is called when an error occurs"""
        print('Error: ' + repr(status_code))
        return False

    def on_data(self, data):
        """This will be called each time we receive stream data"""
        client = MongoClient('localhost', 27017)
        db = client.tweetsdb
        datajson = json.loads(data)
        

        # We only want to store tweets in English because of Sentiment Analyzer
        if "lang" in datajson and datajson["lang"] == "en":
            db.tweetscollection.insert(datajson)


CONSUMER_KEY = "cue6yOS0gH1lQ9XYRfSvt7zPD"
CONSUMER_SECRET = "OTSlghuTGdDwMlG4N7twuEPtZDBdjqpAlEZtQDARTYGvVs1YEh"
ACCESS_TOKEN = "793906953755951105-gvQ7tqhU7g2wwfcw1yw96zGGGcjiHfa"
ACCESS_TOKEN_SECRET = "8pGfOsYfgd3mVY3SVi8tAWukPLg7htePEFOgyaCmIQBXS"

KEYWORDS_BTC_PATH = 'filter_words.txt'


#Authenticating
auth1 = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth1.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

l = StreamListener(api=tweepy.API(wait_on_rate_limit=True))
streamer = tweepy.Stream(auth=auth1, listener=l)
with open(KEYWORDS_BTC_PATH) as f:
    streamer.filter(track=[line.strip() for line in f])
