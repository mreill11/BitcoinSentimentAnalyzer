import json
import ccxt

binance = ccxt.binance()
bitmex = ccxt.bitmex()

bitmex_ticker = bitmex.fetch_ticker('BTC/USD')
current_bid = bitmex_ticker['bid']
print(current_bid)
