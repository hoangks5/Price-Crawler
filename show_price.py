import matplotlib.pyplot as plt
import pymongo
import time
import certifi
import numpy as np

TOKENS = ['BTC-USD', 'ETH-USD', 'DOGE-USD', 'LINK-USD',  'SOL-USD', 'MATIC-USD',  'DOT-USD', 'ATOM-USD']


myclient = pymongo.MongoClient("mongodb+srv://hoangks5:YrfvDz4Mt8xrrHxi@cluster0.tcbxc.mongodb.net/",tlsCAFile=certifi.where())
mydb = myclient['price']
mycol = mydb['datanew']
 
def main(token):
    datas = mycol.find({})
    median = []
    vwa = []
    coinbase = []
    chainlink = []
    timestamp = []
    for data in datas: 
        if data['data']['token'] == token:
            median.append(data['data']['price_median'])
            vwa.append(data['data']['price_volume_weighted_average'])
            coinbase.append(data['data']['coinbase'])
            chainlink.append(data['data']['chainlink'])
            timestamp.append(data['data']['timestamp'])
    median = np.array(median)
    vwa = np.array(vwa)
    chainlink = np.array(chainlink)
    timestamp = np.array(timestamp)
    coinbase = np.array(coinbase)
    plt.subplot(2,4,TOKENS.index(token)+1)
    plt.plot(timestamp,median,timestamp,vwa,timestamp,coinbase,timestamp,chainlink)
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
    for data in datas:
        if data['data']['token'] == token:
            median.append(data['data']['price_median'])
            vwa.append(data['data']['price_volume_weighted_average'])
            coinbase.append(data['data']['coinbase'])
            chainlink.append(data['data']['chainlink'])
            timestamp.append(data['data']['timestamp'])
            price_min.append(data[)

    median = np.array(median)
    vwa = np.array(vwa)
    chainlink = np.array(chainlink)
    timestamp = np.array(timestamp)
    coinbase = np.array(coinbase)
    plt.plot(timestamp,median,timestamp,vwa,timestamp,coinbase,timestamp,chainlink)
    plt.title(token.split('-')[0])
    plt.ylabel('USD')
    frame = plt.gca()
    frame.axes.get_xaxis().set_visible(False)



for token in TOKENS:
    main(token)
plt.gca().legend(('Median','Volume Weighted Average','Coinbase','Chainlink'))
plt.show()