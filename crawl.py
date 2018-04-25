#!/usr/bin/env python
from __future__ import print_function
import tweepy
import urllib
import json
import re
import time
from pymongo import MongoClient
import pymongo
import nltk
from nltk.classify import NaiveBayesClassifier
from tweepy import OAuthHandler
from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import ccxt
nltk.download('vader_lexicon')

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
        # client = MongoClient('localhost', 27017)
        # db = client.tweetsdb
        datajson = json.loads(data)


        # We only want to store tweets in English because of Sentiment Analyzer
        if "lang" in datajson and datajson["lang"] == "en" and "created_at" in datajson:
            #db.tweetscollection.insert(datajson)
            tweet = clean_tweet(datajson["text"])
            if not tweet.startswith('RT') and not detect_ad(tweet):
                process_tweet(tweet, datajson["created_at"])
                #tweetfile.write(tweet + "\n")

def detect_ad(tweet):
    adwords = ["FREE", "install", "don't miss out", "install now", "BONUS", "PRICE WATCH"]
    for word in adwords:
        if word.upper() in tweet.upper():
            return True
    return False

def format_tweet(tweet):    # Tokenizes tweet into indivual words
    return({word: True for word in nltk.word_tokenize(tweet)})

def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def getTextBlobSentiment(tweet):         # TEXTBLOB SENTIMENT ANALYZER
    # create TextBlob object of passed tweet text
    analysis = TextBlob(clean_tweet(tweet))
    # set sentiment
    return analysis.sentiment.polarity

def vader_sentiment_analyzer(tweet):
    vader_analyzer = SentimentIntensityAnalyzer()
    vs = vader_analyzer.polarity_scores(tweet)
    return vs['compound']

def process_tweet(tweet, created_at):
    global TICKER
    global current_btc_bid
    TICKER = TICKER + 1
    textblob_sentiment = getTextBlobSentiment(tweet)
    vader_sentiment = vader_sentiment_analyzer(tweet)
    avg_sentiment_score = (textblob_sentiment + vader_sentiment) / 2.0
    ts = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(created_at,'%a %b %d %H:%M:%S +0000 %Y'))
    if TICKER % 100 == 0:
        current_btc_bid = get_btc_bid()
    data = {}
    data["sentiment"] = avg_sentiment_score
    data["time"] = ts
    data["btc_bid"] = current_btc_bid
    json_string = json.dumps(data)
    store_tweet(json_string)
    print(json_string)

def store_tweet(data):
    client = MongoClient("mongodb+srv://db_admin:Edgew00d!@cluster0-b82dm.mongodb.net/tweetsdb")
    db = client.tweetsdb
    collection = db.sentiment_collection
    collection.insert(json.loads(data))

def get_btc_bid():
    bitmex_ticker = bitmex.fetch_ticker('BTC/USD')
    return bitmex_ticker['bid']

CONSUMER_KEY = "fuOzrcFr92XQDjsUa7cwUJtUZ"
CONSUMER_SECRET = "kMKsMx9WEuwNHztEWTPns8OT6hvL2858vILLAImY3isBfMm0vB"
ACCESS_TOKEN = "2677412642-e6FMkXhJIWPL5kd6MCNccKNjkF53v8j3atuJDJY"
ACCESS_TOKEN_SECRET = "Xsglk8QuAVLE1WVtkfFdq8wWl0O9AY4cVdLpcTkXOI21w"

KEYWORDS_BTC_PATH = 'data/filter_words.txt'

TICKER = 0
bitmex = ccxt.bitmex()
current_btc_bid = get_btc_bid()

#Authenticating
auth1 = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth1.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

l = StreamListener(api=tweepy.API(wait_on_rate_limit=True))
streamer = tweepy.Stream(auth=auth1, listener=l)
with open(KEYWORDS_BTC_PATH) as f:
    streamer.filter(track=[line.strip() for line in f])
