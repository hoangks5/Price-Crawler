import requests
import time
import pymongo
import threading
import certifi
from datetime import datetime
import numpy as np
from flask import Flask
import json
from flask_cors import CORS
import random
# BTC-USD, ETH-USD, BNB-USD, DOGE-USD, LINK-USD, UNI-USD, SOL-USD, MATIC-USD, LUNA-USD, DOT-USD, ATOM-USD
# Connection MongoDB


#myclient = pymongo.MongoClient("mongodb+srv://hoangks5:YrfvDz4Mt8xrrHxi@cluster0.tcbxc.mongodb.net/?retryWrites=true&w=majority")
#mydb = myclient["price"]
LOGGING_FAIL = 'No'
#client = pymongo.MongoClient("mongodb+srv://hoangks5:YrfvDz4Mt8xrrHxi@cluster0.tcbxc.mongodb.net/",tlsCAFile=certifi.where())
#mydb = client['price']
#mycol = mydb['data']
TOKENS = ['BTC-USD', 'ETH-USD', 'BNB-USD', 'DOGE-USD', 'LINK-USD', 'UNI-USD', 'SOL-USD', 'MATIC-USD', 'LUNA-USD', 'DOT-USD', 'ATOM-USD']


# BINANCE

# Doc: https://binance-docs.github.io/apidocs/spot/en/#24hr-ticker-price-change-statistics

# Ex:
    # API: https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT
    # DEX: https://www.binance.com/en/trade/BTC_USDT?theme=dark&type=spot

# Note: 
    # Volume24: USDT (symbol)
    # Pair: USDT
    # Timestamp : Realtime


def get_binance_price(symbol): 
    symbol = symbol.split("-")[0]
    url = "https://api.binance.com/api/v3/ticker/24hr?symbol="+symbol+"USDT"
    time_start = time.time()
    response = requests.get(url)
    time_stop = time.time()
    avg = {
        'token': symbol,
        'source': 'BINACE',
        'timestamp': time_start,
        'price': float(response.json()['lastPrice']),
        'volume24h': float(response.json()['quoteVolume']),
        'delay': time_stop - time_start
    }
    return avg
     
    

# COINBASE

# Doc: https://docs.cloud.coinbase.com/exchange/reference/exchangerestapi_getproductticker

# Ex: 
    # API: https://api.exchange.coinbase.com/products/BTC-USDT/stats
    # DEX: https://pro.coinbase.com/trade/BTC-USDT

# Note: 
    # Volume24h: BTC 
    # Pair: USDT, USD
    # Timestamp: Realtime


def get_coinbase_price(symbol):
    url = "https://api.exchange.coinbase.com/products/"+symbol+"T/stats"
    headers = {"Accept": "application/json"}
    response = requests.get(url, headers=headers)
    time_start = time.time()
    response = requests.request("GET", url, headers=headers)
    time_stop = time.time()
    try:
        avg = {
            'token': symbol.split('-')[0],
            'source': 'COINBASE',
            'timestamp': time_start,
            'price': float(response.json()['last']),
            'volume24h': float(response.json()['volume']),
            'delay': time_stop-time_start
        }
        return avg
    except:
        pass
    
    

# GATEIO

# Doc: https://api.gateio.ws/api2#ticker

# Ex:
    # API: https://data.gateapi.io/api2/1/ticker/BTC_USDT
    # DEX: https://www.gate.io/trade/BTC_USDT

# Note: 
    # Volume24h: USDT
    # Pair: USDT, USD
    # Timestamp: Realtime

def get_gateio_price(symbol):
    pair = symbol.replace("-","_")
    url = "https://data.gateapi.io/api2/1/ticker/"+pair+'t'
    time_start = time.time()
    response = requests.get(url)
    time_stop = time.time()
    try:
        avg = {
            'token': symbol.split('-')[0],
            'source': 'GATEIO',
            'timestamp': time_start,
            'price': float(response.json()['last']),
            'volume24h': float(response.json()['baseVolume']),
            'delay': time_stop - time_start
        }
        return avg
    except:
        pass
    
    
# KUCOIN 

# Doc: https://docs.kucoin.com/#get-24hr-stats

# Ex:
    # API: https://api.kucoin.com/api/v1/market/stats?symbol=BTC-USDT
    # DEX: https://www.kucoin.com/trade/BTC-USDT

# Note: 
    # Volume24h: USDT(*)
    # Pair: USDT
    # Timestamp: (1-2s)
def get_kucoin_price(symbol):
    
    time_start = time.time()
    response = requests.get('https://api.kucoin.com/api/v1/market/stats?symbol='+symbol+'T')
    avg = {
        'token': symbol.split('-')[0],
        'source': 'KUCOIN',
        'timestamp': response.json()['data']['time']/1000,
        'price': float(response.json()['data']['last']),
        'volume24h': float(response.json()['data']['volValue']),
        'delay': time_start - response.json()['data']['time']/1000
    }
    return avg
    
    
    
    
# COINMARKETCAP

# Doc: https://coinmarketcap.com/api/documentation/v1/#operation/getV1CryptocurrencyQuotesLatest

# Ex:
    # API: https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest
    # DEX: https://coinmarketcap.com/currencies/bitcoin/

# Note: 
    # Volume24h: USD
    # Pair: USD
    # Timestamp: (100-1000s)


def get_coinmarketcap_price(symbol):
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    parameters = {
        'symbol' : symbol.split('-')[0]
    }
    header = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY' : '3fe6464e-8a86-4ad7-8c95-d7beaef15bad'}
    time_start = time.time()
    response = requests.get(url=url,params=parameters,headers=header)
    avg = {
        'token': symbol.split('-')[0],
        'source': 'COINMARKERTCAP',
        'timestamp': datetime.strptime(response.json()['data'][symbol.split('-')[0]]['last_updated'],
        '%Y-%m-%dT%H:%M:%S.%f%z').timestamp(),
        'price': response.json()['data'][symbol.split('-')[0]]['quote']['USD']['price'],
        'volume24h': response.json()['data'][symbol.split('-')[0]]['quote']['USD']['volume_24h'],
        'delay': time_start - datetime.strptime(response.json()['data'][symbol.split('-')[0]]['last_updated'],
        '%Y-%m-%dT%H:%M:%S.%f%z').timestamp()
    }
    
    return avg
    

# COINGECKO

# Docs: https://www.coingecko.com/en/api/documentation
#       https://github.com/man-c/pycoingecko

# Ex:
    # API: https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_24hr_vol=true&include_last_updated_at=true
    # DEX: https://www.coingecko.com/en/coins/bitcoin

# Note: 
    # Volume24h: USD
    # Pair: USD
    # Timestamp: (30-60s)

TOKEN_IDS_COINGECKO = {'BTC': 'bitcoin',
                        'ETH': 'ethereum',
                        'BNB': 'binancecoin',
                        'DOGE': 'dogecoin',
                        'LINK': 'chainlink',
                        'UNI': 'uniswap',
                        'SOL': 'solana',
                        'MATIC': 'matic-network',
                        'LUNA': 'terra-luna-2',
                        'DOT': 'polkadot',
                        'ATOM': 'cosmos'}



def get_coingecko_price(symbol):
    token = symbol.split('-')[0]
    symbol = TOKEN_IDS_COINGECKO[symbol.split("-")[0]]
    url = "https://api.coingecko.com/api/v3/simple/price?ids="+symbol+"&vs_currencies=usd&include_24hr_vol=true&include_last_updated_at=true"
    time_start = time.time()
    response = requests.get(url)

    avg = {
        'token': token,
        'source': 'COINGECKO',
        'timestamp': response.json()[symbol]['last_updated_at'],
        'price': response.json()[symbol]['usd'],
        'volume24h': response.json()[symbol]['usd_24h_vol'],
        'delay': time_start - response.json()[symbol]['last_updated_at']
    }
    return avg
    
# CHAINLINK

# Doc: https://docs.chain.link/docs/single-word-response/

# Ex:
    # API: https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC&tsyms=USDT
    # DEX: No

# Note:
    # Volume24h: USDT
    # Pair: USDT, USD
    # Timestamp: (1-10s)


def get_chainlink_price(symbol):
    
    url = 'https://min-api.cryptocompare.com/data/pricemultifull?fsyms='+symbol.split('-')[0]+'&tsyms='+symbol.split('-')[1]+'t'
    time_start = time.time()
    response = requests.get(url)

    avg = {
        'token': symbol.split('-')[0],
        'source': 'CHAINLINK',
        'timestamp': response.json()['RAW'][symbol.split('-')[0]]['USDT']['LASTUPDATE'],
        'price': response.json()['RAW'][symbol.split('-')[0]]['USDT']['PRICE'],
        'volume24h': response.json()['RAW'][symbol.split('-')[0]]['USDT']['VOLUME24HOURTO'],
        'delay': time_start - response.json()['RAW'][symbol.split('-')[0]]['USDT']['LASTUPDATE']
    }
    return avg
   

def cal_median(docs):
    median = 0
    for row in docs:
        median += row['price']
    return median/len(docs)
    
def cal_volume_weighted_average(docs):
    total_price = 0
    total_volume = 0
    for row in docs:
        # total_price = E(price*volume24h)/E(volume24h)
        total_price += row['price']*row['volume24h']
        total_volume += row['volume24h']
    return total_price/total_volume

def median(token):
    timest = time.time()
    docs = []
    token = token.upper()+'-USD'
    th = []
    def t1(token):
            docs.append(get_binance_price(token))
    def t2(token):
            docs.append(get_coinbase_price(token))
    def t3(token):
            docs.append(get_chainlink_price(token))
    def t4(token):
            docs.append(get_kucoin_price(token))
    def t5(token):
            docs.append(get_coinmarketcap_price(token))
    def t6(token):
            docs.append(get_coingecko_price(token))
    def t7(token):
            docs.append(get_gateio_price(token))
    th.append(threading.Thread(target=t1,args={token,}))
    th.append(threading.Thread(target=t2,args={token,}))
    th.append(threading.Thread(target=t3,args={token,}))
    th.append(threading.Thread(target=t4,args={token,}))
    th.append(threading.Thread(target=t5,args={token,}))
    th.append(threading.Thread(target=t6,args={token,}))
    th.append(threading.Thread(target=t7,args={token,}))
    for ths in th:
        ths.start()
    for ths in th:
        ths.join()
    req = []
    for val in docs:
        if val != None :
            req.append(val)
    docs = req
    data = {
        'token' : token,
        'timestamp' : timest,
        'price_median' : cal_median(docs)
    }
    return data
 

def vwa(token):
    timest = time.time()
    docs = []
    token = token.upper()+'-USD'
    th = []
    def t1(token): 
            docs.append(get_binance_price(token))
    def t2(token):
            docs.append(get_coinbase_price(token))
    def t3(token):
            docs.append(get_chainlink_price(token))
    def t4(token):
            docs.append(get_kucoin_price(token))
    def t5(token):
            docs.append(get_coinmarketcap_price(token))
    def t6(token):
            docs.append(get_coingecko_price(token))
    def t7(token):
            docs.append(get_gateio_price(token))
    th.append(threading.Thread(target=t1,args={token,}))
    th.append(threading.Thread(target=t2,args={token,}))
    th.append(threading.Thread(target=t3,args={token,}))
    th.append(threading.Thread(target=t4,args={token,}))
    th.append(threading.Thread(target=t5,args={token,}))
    th.append(threading.Thread(target=t6,args={token,}))
    th.append(threading.Thread(target=t7,args={token,}))
    for ths in th:
        ths.start()
    for ths in th:
        ths.join()
    req = []
    for val in docs:
        if val != None :
            req.append(val)
    docs = req
    data = {
        'token' : token,
        'timestamp' : timest,
        'price_volume_weighted_average' : cal_volume_weighted_average(docs)
    }
    return data

def cal_gaussian_noise(docs):
    req = []
    for val in docs:
        if val != None :
            req.append(val['price'])
    # https://numpy.org/doc/stable/reference/random/generated/numpy.random.normal.html
    return np.random.normal(np.mean(req),np.std(req),1)[0]


def choice_max(docs):
    req = []
    for val in docs:
        if val != None :
            req.append(val['price'])
    return max(req)

def choice_min(docs):
    req = [] 
    for val in docs:
        if val != None :
            req.append(val['price'])
    return min(req)
        

def test(token):
    timest = time.time()
    docs = []
    token = token.upper()+'-USD'
    th = []
    price_coinbase = []
    price_chainlink = []
    def t1(token):
            docs.append(get_binance_price(token))
    def t2(token):
            docs.append(get_coinbase_price(token))
    def t3(token):
            docs.append(get_chainlink_price(token))
    def t4(token):
            docs.append(get_kucoin_price(token))
    def t5(token):
            docs.append(get_coinmarketcap_price(token))
    def t6(token):
            docs.append(get_coingecko_price(token))
    def t7(token):
            docs.append(get_gateio_price(token))
    def t8(token):
        price_coinbase.append(get_coinbase_price(token)['price'])
    def t9(token):
        price_chainlink.append(get_chainlink_price(token)['price'])
    th.append(threading.Thread(target=t1,args={token,}))
    th.append(threading.Thread(target=t2,args={token,}))
    th.append(threading.Thread(target=t3,args={token,}))
    th.append(threading.Thread(target=t4,args={token,}))
    th.append(threading.Thread(target=t5,args={token,}))
    th.append(threading.Thread(target=t6,args={token,}))
    th.append(threading.Thread(target=t7,args={token,}))
    th.append(threading.Thread(target=t8,args={token,}))
    th.append(threading.Thread(target=t9,args={token,}))
    for ths in th:
        ths.start()
    for ths in th:
        ths.join()
    data = {
        'data' : docs,
        'token' : token,
        'timestamp' : timest,
        'price_median' : cal_median(docs),
        'price_volume_weighted_average' : cal_volume_weighted_average(docs),
        'price_coinbase' : price_coinbase[0],
        'price_chainlink' : price_chainlink[0],
        'price_gaussian_noise' : cal_gaussian_noise(docs),
        'price_max' : choice_max(docs),
        'price_min' : choice_min(docs)
    }
    return data




