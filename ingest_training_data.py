import csv

pos_tweets = open('pos_tweets.txt', 'w')
neg_tweets = open('neg_tweets.txt', 'w')

with open('training_data.csv', 'r') as f:
    reader = csv.reader(f)
    tweet_list = list(reader)

for tweet in tweet_list:
    if tweet[1] == 0:
        neg_tweets.write(str(tweet[3]) + "\n")
    else:
        pos_tweets.write(str(tweet[3]) + "\n")

pos_tweets.close()
neg_tweets.close()
