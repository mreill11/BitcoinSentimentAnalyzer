This is a Bitcoin market sentiment analyzer that uses various sentiment analysis methods to evaluate the Twitter ecosystem and produce valuable insights from the tweets we analyze. It consists of two main parts:

1. The Crawler gathers Twitter data using the Stream API and Bitcoin price data using the Bitmex Exchange API. It stores this data in MongoDB as a tuple <sentiment, btc_price, datetime>.

2. The plotter uses the Plotly Python package to plot the sentiments and BTC prices on a single graph to allow for comparison.

The plotter will plot whatever data you have in your MongoDB, so if you wish to implement the analyzer you must run the crawler for a while first.
```python crawl.py```
