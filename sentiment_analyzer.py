import re
import tweepy
import pymongo
import nltk
from nltk.classify import NaiveBayesClassifier
from tweepy import OAuthHandler
from textblob import TextBlob

def format_tweet(tweet):    # Tokenizes tweet into indivual words
    return({word: True for word in nltk.word_tokenize(tweet)})

def clean_tweet(tweet):
    '''
    Utility function to clean tweet text by removing links, special characters
    using simple regex statements.
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def get_tweet_sentiment(tweet):         # TEXTBLOB SENTIMENT ANALYZER
    '''
    Utility function to classify sentiment of passed tweet
    using textblob's sentiment method
    '''
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
    '''
    Main function to fetch tweets and parse them.
    '''
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
            parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

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

def main():
    # print("POSITIVE:\n")
    #
    # with open("./pos_tweets.txt") as f:
    #     for i in f:
    #         print(get_tweet_sentiment(i))
    #
    # print("NEGATIVE:\n")
    # with open("./neg_tweets.txt") as f:
    #     for i in f:
    #         print(get_tweet_sentiment(i))

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
    # print("Dumping my BTC. Not looking good." + " - " + get_tweet_sentiment("Dumping my BTC. Not looking good."))
    # print("Selling my bitcoins" + " - " + get_tweet_sentiment("Selling my bitcoins"))
    # print("Loving my bitcoins never getting rid of them" + " - " + get_tweet_sentiment("Loving my bitcoins never getting rid of them"))
    # print("I hate bitcoin" + " - " + get_tweet_sentiment("I hate bitcoin"))
    # picking positive tweets from tweets
    # ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    # print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))
    # ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    # print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))
    # print("Neutral tweets percentage: {} %".format(100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets)))

if __name__ == "__main__":
    # calling main function
    main()
