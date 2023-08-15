import requests
import pandas as pd
import yfinance as yf
import datetime as dt
from requests_html import HTMLSession
import queue
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import sqlalchemy

session = HTMLSession()
num_currencies=250
resp = session.get(f"https://finance.yahoo.com/crypto?offset=0&count={num_currencies}")
tables = pd.read_html(resp.html.raw_html)               
df = tables[0].copy()
symbols_yf = df.Symbol.tolist()

symdf = pd.DataFrame(symbols_yf)




engine = sqlalchemy.create_engine('mssql+pyodbc://@' + 'LOUIS-PC' + '/' + 'Crypto_market_prices' + '?trusted_connection=yes&driver=ODBC Driver 17 for SQL Server')
    
symdf.to_sql('symbols', engine,if_exists='append')