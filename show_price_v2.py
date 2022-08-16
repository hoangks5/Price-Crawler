import matplotlib.pyplot as plt
import pymongo
import time
import certifi
import numpy as np

TOKENS = ['BTC-USD', 'ETH-USD', 'DOGE-USD', 'LINK-USD',  'SOL-USD', 'MATIC-USD',  'DOT-USD', 'ATOM-USD']


myclient = pymongo.MongoClient("mongodb+srv://hoangks5:YrfvDz4Mt8xrrHxi@cluster0.tcbxc.mongodb.net/",tlsCAFile=certifi.where())
mydb = myclient['price']
mycol = mydb['datanew']
 
def coinbase_benmark(token): 
    datas = mycol.find({})
    median = [] 
    vwa = []
    coinbase = []
    timestamp = []
    price_min = []
    price_max = []
    price_noise = []
    for data in datas: 
        if data['data']['token'] == token:
            median.append(data['data']['price_median'])
            vwa.append(data['data']['price_volume_weighted_average'])
            coinbase.append(data['data']['price_coinbase'])
            timestamp.append(data['data']['timestamp'])
            price_min.append(data['data']['price_min'])
            price_max.append(data['data']['price_max'])
            price_noise.append(data['data']['price_gaussian_noise'])
    median = np.array(median) - np.array(coinbase)
    vwa = np.array(vwa)
    chainlink = np.array(chainlink)
    timestamp = np.array(timestamp)
    coinbase = np.array(coinbase) 
    plt.subplot(2,4,TOKENS.index(token)+1)
    plt.plot(timestamp,median,timestamp,vwa,timestamp,coinbase,timestamp,chainlink,timestamp,price_max,timestamp,price_min,timestamp,price_noise)
    plt.title(token.split('-')[0])
    plt.ylabel('USD')
    frame = plt.gca()
    frame.axes.get_xaxis().set_visible(False) 



def main1(token):
    datas = mycol.find({})
    median = []
    vwa = []
    coinbase = []
    chainlink = []
    timestamp = []
    price_min = []
    price_max = []
    price_noise = []
    for data in datas:
        if data['data']['token'] == token:
            median.append(data['data']['price_median'])
            vwa.append(data['data']['price_volume_weighted_average'])
            coinbase.append(data['data']['price_coinbase'])
            chainlink.append(data['data']['price_chainlink'])
            timestamp.append(data['data']['timestamp'])
            price_min.append(data['data']['price_min'])
            price_max.append(data['data']['price_max'])
            price_noise.append(data['data']['price_gaussian_noise'])
    median = np.array(median)
    vwa = np.array(vwa)
    chainlink = np.array(chainlink)
    timestamp = np.array(timestamp)
    coinbase = np.array(coinbase)
    plt.plot(timestamp,median,timestamp,vwa,timestamp,coinbase,timestamp,chainlink,
            timestamp,price_min,timestamp,price_max,timestamp,price_noise)
    plt.title(token.split('-')[0])
    plt.ylabel('USD')
    frame = plt.gca()
    frame.axes.get_xaxis().set_visible(False)
for token in TOKENS:
    coinbase_benmark(token)
plt.gca().legend(('Median','Volume Weighted Average','Coinbase','Chainlink','Min','Max','Noise'))
plt.show()