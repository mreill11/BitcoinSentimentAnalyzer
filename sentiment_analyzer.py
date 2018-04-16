import re
import tweepy
import pymongo
import nltk
from nltk.classify import NaiveBayesClassifier
from tweepy import OAuthHandler
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def format_tweet(tweet):    # Tokenizes tweet into indivual words
    return({word: True for word in nltk.word_tokenize(tweet)})

def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def getTextBlobSentiment(tweet):         # TEXTBLOB SENTIMENT ANALYZER
    # create TextBlob object of passed tweet text
    analysis = TextBlob(clean_tweet(tweet))
    # set sentiment
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'

def get_tweets(self, query, count = 10):
    # empty list to store parsed tweets
    tweets = []

    try:
        # call twitter api to fetch tweets
        fetched_tweets = self.api.search(q = query, count = count)

        # parsing tweets one by one
        for tweet in fetched_tweets:
            # empty dictionary to store required params of a tweet
            parsed_tweet = {}
            # saving text of tweet
            parsed_tweet['text'] = tweet.text
            # saving sentiment of tweet
            parsed_tweet['sentiment'] = self.getTextBlobSentiment(tweet.text)

            # appending parsed tweet to tweets list
            if tweet.retweet_count > 0:
                # if tweet has retweets, ensure that it is appended only once
                if parsed_tweet not in tweets:
                    tweets.append(parsed_tweet)
            else:
                tweets.append(parsed_tweet)
        # return parsed tweets
        store_tweets(tweets)
        return tweets

    except tweepy.TweepError as e:
        # print error (if any)
        print("Error : " + str(e))

def vader_sentiment_analyzer(tweet):
    vader_analyzer = SentimentIntensityAnalyzer()
    vs = vader_analyzer.polarity_scores(tweet)
    return vs

def main():
    pos = []
    with open("./pos_tweets.txt") as f:
        for i in f:
            pos.append([format_tweet(i), 'pos'])

    neg = []
    with open("./neg_tweets.txt") as f:
        for i in f:
            neg.append([format_tweet(i), 'neg'])

    # next, split labeled data into the training and test data
    training = pos[:int((.8)*len(pos))] + neg[:int((.8)*len(neg))]
    test = pos[int((.8)*len(pos)):] + neg[int((.8)*len(neg)):]
    # training = pos + neg

    classifier = NaiveBayesClassifier.train(training)
    classifier.show_most_informative_features()

    vader_analyzer = SentimentIntensityAnalyzer()
    for sentence in sentences:
        vs = vader_analyzer.polarity_scores(sentence)
        print("{:-<65} {}".format(sentence, str(vs)))

if __name__ == "__main__":
    # calling main function
    main()
