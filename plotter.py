import plotly.plotly as py
import plotly.graph_objs as go

from datetime import datetime
from pymongo import MongoClient
import pandas_datareader.data as web

FREQ = 200

sentiments = []
compressed_sentiments = []
datetimes = []
compressed_datetimes = []
client = MongoClient('localhost', 27017)
db = client['tweetsdb']
collection = db['sentiment_collection']
cursor = collection.find({})
for document in cursor:
    sentiments.append(document['sentiment'])
    datetimes.append(document['time'])

count = 0
avg = 0
for sentiment in sentiments:
    count = count + 1
    avg = avg + sentiment
    if count % FREQ == 0:
        compressed_sentiments.append(avg / float(FREQ))
        compressed_datetimes.append(datetimes[count])
        avg = 0.0

data = [go.Scatter(x=compressed_datetimes, y=compressed_sentiments)]
py.iplot(data, filename='sentiment-time-series')
