import requests
import pandas as pd
import yfinance as yf
import datetime as dt
from requests_html import HTMLSession
import queue
from store import Storage


class handler:
    def __init__(self, Q):
        self.q = Q

    def yfinance_data(self):

        session = HTMLSession()
        num_currencies=250
        resp = session.get(f"https://finance.yahoo.com/crypto?offset=0&count={num_currencies}")
        tables = pd.read_html(resp.html.raw_html)               
        df = tables[0].copy()
        symbols_yf = df.Symbol.tolist()
        start = dt.datetime(2020,1,1)
        end = dt.datetime.now()
        marketdata = yf.download(symbols_yf, start, end)
        df = marketdata.stack(level=1).rename_axis(['Date', 'Ticker']).reset_index(level=0)
        df= df.reset_index()
        
        self.put_on_q(df)


    def put_on_q(self,data):
        self.q.put(item= data)

    def q_check(self,q):
        if q.full:
            print('the queue is full')
        else:
            print('queue is empty')

    def binance_data(self):
        pass

    def coin_market_cap(self):
        pass


import configparser






def main():
   config = configparser.RawConfigParser()
   configFilePath = r'C:\Users\louie\crypto_trade\config.cfg'
   config.read(configFilePath)
   q = queue.Queue()
   
  
   
   

if __name__ == "__main__":
    main()


