import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np
from scipy.interpolate import interp1d
from datetime import datetime
from pymongo import MongoClient
import pandas_datareader.data as web
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import signal
FREQ = 2000

sentiments = []
compressed_sentiments = []
datetimes = []
compressed_datetimes = []
btc_bids = []
btc_bid_datetimes = []
client = MongoClient("mongodb+srv://db_admin:Edgew00d!@cluster0-b82dm.mongodb.net/tweetsdb")
db = client.tweetsdb
sentiment_collection = db.sentiment_collection

cursor = sentiment_collection.find({})
for document in cursor:
    sentiments.append(document['sentiment'])
    datetimes.append(document['time'])
    if "btc_bid" in document and document['btc_bid'] != 0:
        btc_bids.append(document['btc_bid'])
        btc_bid_datetimes.append(document['time'])

count = 0
avg = 0
for sentiment in sentiments:
    count = count + 1
    avg = avg + sentiment
    if count % FREQ == 0:
        compressed_sentiments.append((avg) / float(FREQ))
        compressed_datetimes.append(datetimes[count])
        avg = 0.0
#pd_datetimes = np.array(compressed_datetimes)
#pd_sentiments = np.array(compressed_sentiments)
#interpolated_datetimes = np.linspace(pd_sentiments.min(), pd_sentiments.max(), 300)
#interpolated_sentiments = interp1d(pd_datetimes, pd_sentiments)
#smooth_sentiments = spline(pd_sentiments, compressed_datetimes, interpolated_datetimes)
twitter_sentiment = go.Scatter(
                x=compressed_datetimes,
                y=signal.savgol_filter(compressed_sentiments, 53, 3),
                name = "Twitter Sentiment",
                line = dict(color = '#17BECF'),
                opacity = 0.8,
                yaxis = 'y2')

btc_price = go.Scatter(
                x=btc_bid_datetimes,
                y=btc_bids,
                name = "BTC Price",
                line = dict(color = '#7F7F7F'),
                opacity = 0.8)

layout = go.Layout(
    title='Bitcoin Price vs Twitter Sentiment',
    yaxis=dict(
        title='Bitcoin Price (USD)',
        titlefont=dict(
            color='#7F7F7F'
        ),
        tickfont=dict(
            color='#7F7F7F'
        )
    ),
    yaxis2=dict(
        title='Twitter Sentiment',
        titlefont=dict(
            color='#17BECF'
        ),
        tickfont=dict(
            color='#17BECF'
        ),
        overlaying='y',
        side='right'
    )
)

data = [twitter_sentiment, btc_price]
fig = go.Figure(data=data, layout=layout)
py.plot(fig)
