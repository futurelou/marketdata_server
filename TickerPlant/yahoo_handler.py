import requests
import pandas as pd
import yfinance as yf
import datetime as dt
from datetime import timedelta
import queue
from store import Storage
from symbols import Symbol_map
import configparser
import threading 
import time


class Handler:
    def __init__(self, Q, symbols):
        self.q = Q
        self.symbol = symbols
        self.started = False        

    def put_on_q(self,data):
        self.q.put(item= data)

    def q_check(self,q):
        if q.full:
            print('the queue is full')
        else:
            print('queue is empty')

    def start(self):
        self.started = True

    def stop(self):
        self.started = False

    def run(self):
        self.start()
        while self.started :
           
            result = self.get_live_data()
            self.put_on_q(result)
            time.sleep(60)


class Yahoo_handler(Handler):

    def get_hist_data(self):
            start =  dt.datetime.now() - timedelta(days = 729)
            
            end = dt.datetime.now()
            symdf = self.symbol.get_symbols()
            symlist = symdf['0'].to_list()
            marketdata = yf.download(symlist, start, end, interval='1h')
            df = marketdata.stack(level=1).rename_axis(['Date', 'Ticker']).reset_index(level=0)
            df= df.reset_index()
            return df


    def get_live_data(self):

        start =  dt.datetime.now() - timedelta(minutes= 1)
        end = dt.datetime.now()
        symdf = self.symbol.get_symbols()
        symlist = symdf['0'].to_list()
        marketdata = yf.download(symlist, start, end, interval='1m')
        df = marketdata.stack(level=1).rename_axis(['Date', 'Ticker']).reset_index(level=0)
        df= df.reset_index()
        return df

    


class binance_data(Handler):

    pass

class coin_market_cap(Handler):
    pass

class twitter_sentiment(Handler):
    pass 


def main():
   config = configparser.RawConfigParser()
   configFilePath = r'C:\Users\louie\crypto_trade\config.cfg'
   config.read(configFilePath)
   q = queue.Queue()
   y = Symbol_map(feedType='DB', dbConnection=('LOUIS-PC', 'Crypto_market_prices'), dbtype="MSSQL")
   x = Yahoo_handler(Q=q, symbols=y)
   z = Storage(q,'csv')
   params = (config['FILEPATH']['Crypto_Data'], '1_hour_interval_crypto_data')
   threading.Thread(target=x.run).start()

   z.run(params)
  





  
   
  
   
   

if __name__ == "__main__":
    main()



