tweetsfile = open("tweets.txt", 'r')

positive_tweets = open("pos_tweets.txt", 'a')
neutral_tweets = open("neut_tweets.txt", 'a')
negative_tweets = open("neg_tweets.txt", 'a')

inputs = ["-1", "0", "1"]
for line in tweetsfile:
    print(line)
    classification = input("pos: 1 __ neutr: 0 __ neg: -1 : ")
    if classification == "1":
        positive_tweets.write(line)
    elif classification == "0":
        neutral_tweets.write(line)
    elif classification == "-1":
        negative_tweets.write(line)
    else:
        continue
