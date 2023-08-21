import requests
import pandas as pd
import yfinance as yf
import datetime as dt
from datetime import timedelta
import queue
from store import Storage
from symbols import Symbol_map
import configparser


class handler:
    def __init__(self, Q, symbols):
        self.q = Q
        self.symbol = symbols
        self.start = False 
        self.stop = True 

    def put_on_q(self,data):
        self.q.put(item= data)

    def q_check(self,q):
        if q.full:
            print('the queue is full')
        else:
            print('queue is empty')

    def start(self):
        self.start = True

    def stop(self):
        self.stop = False

    def run(self):
        while self.start():
            result = self.get_live_data()
            self.put_on_q(result)


class yahoo_handler(handler):

    def get_hist_data(self):

        start =  dt.datetime.now() - timedelta(days = 730)#dt.datetime(2022,1,1)
        end = dt.datetime.now()
        symdf = self.symbol.get_symbols()
        symlist = symdf['0'].to_list()
        marketdata = yf.download(symlist, start, end, interval='1m')
        df = marketdata.stack(level=1).rename_axis(['Date', 'Ticker']).reset_index(level=0)
        df= df.reset_index()
        return df


    def get_live_data(self):

        start =  dt.datetime.now() - timedelta(minutes= = 1)#dt.datetime(2022,1,1)
        end = dt.datetime.now()
        symdf = self.symbol.get_symbols()
        symlist = symdf['0'].to_list()
        marketdata = yf.download(symlist, start, end, interval='1m')
        df = marketdata.stack(level=1).rename_axis(['Date', 'Ticker']).reset_index(level=0)
        df= df.reset_index()
        return df

    


class binance_data(handler):

    pass


class coin_market_cap(handler):
    pass

class twitter_sentiment(handler):
    pass 


def main():
   config = configparser.RawConfigParser()
   configFilePath = r'C:\Users\louie\crypto_trade\config.cfg'
   config.read(configFilePath)
   q = queue.Queue()
   y = Symbol_map(feedType='DB', dbConnection=('LOUIS-PC', 'Crypto_market_prices'), dbtype="MSSQL")
   x = yahoo_handler(Q=q, symbols=y)
   x.get_data()
   x.q_check(q)
   y = Storage(q)
   y.save_to_csv(path=config['FILEPATH']['Crypto_Data'], filename='test' )
  
   
   

if __name__ == "__main__":
    main()


