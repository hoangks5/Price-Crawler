import requests
import time
import pymongo
import threading
import certifi
from datetime import datetime
import main
# BTC-USD, ETH-USD, BNB-USD, DOGE-USD, LINK-USD, UNI-USD, SOL-USD, MATIC-USD, LUNA-USD, DOT-USD, ATOM-USD
# Connection MongoDB


#myclient = pymongo.MongoClient("mongodb+srv://hoangks5:YrfvDz4Mt8xrrHxi@cluster0.tcbxc.mongodb.net/?retryWrites=true&w=majority")
#mydb = myclient["price"]
 
LOGGING_FAIL = 'No'
client = pymongo.MongoClient("mongodb+srv://hoangks5:YrfvDz4Mt8xrrHxi@cluster0.tcbxc.mongodb.net/",tlsCAFile=certifi.where())
mydb = client['price']
mycol = mydb['datanew']
TOKENS = ['BTC-USD', 'ETH-USD', 'BNB-USD', 'DOGE-USD', 'LINK-USD', 'UNI-USD', 'SOL-USD', 'MATIC-USD', 'LUNA-USD', 'DOT-USD', 'ATOM-USD']


def test(token):
    token =token.split('-')[0]
    h = main.test(token=token)
    print(h)
    #if h['data'] != None:
     #   mycol.insert_one(h)
while True:
    th = []
    for token in TOKENS:
        th.append(threading.Thread(target=test,args={token,}))
    for ths in th:
        ths.start()
    time.sleep(300)