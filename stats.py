from pymongo import MongoClient
import numpy as np
from scipy import stats
from scipy import signal
import pandas as pd
import matplotlib.pyplot as plt
matplotlib.use('Agg')

sentiments = []
datetimes = []
btc_bids = []

client = MongoClient("mongodb+srv://db_admin:Edgew00d!@cluster0-b82dm.mongodb.net/tweetsdb")
db = client.tweetsdb
collection = db.sentiment_collection

count = 0
cursor = collection.find({})
for document in cursor:
    if "btc_bid" in document and document['btc_bid'] != 0:
        sentiments.append(document['sentiment'])
        btc_bids.append(document['btc_bid'])
        count = count + 1
        datetimes.append(document['time'])

print("Total number of datapoints: {}".format(count))
#cross_correlation = np.correlate(sentiments, btc_bids, mode='full')
#print("Cross-correlation: {}".format(cross_correlation))
slope, intercept, r_value, p_value, std_err = stats.linregress(sentiments, btc_bids)
print("Slope: {}\nIntercept: {}\nR: {}\nR-Squared: {}\nP-Value: {}\nStd Error: {}".format(slope, intercept, r_value, r_value**2, p_value, std_err))

filtered_sentiments = scipy.signal.savgol_filter(sentiments, 7, 2)
plot(datetimes, filtered_sentiments)
