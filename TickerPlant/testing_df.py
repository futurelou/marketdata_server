import requests
import pandas as pd
import yfinance as yf
import datetime as dt
from requests_html import HTMLSession
import queue
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

url = 'https://pro-api.coinmarketcap.com/v1/community/trending/token'
parameters = {
  'limit':'1',
  
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': 'a9407896-d389-4042-8729-9fe6c1a7b9ac',
}

session = Session()
session.headers.update(headers)

try:
  response = session.get(url, params=parameters)
  data = json.loads(response.text)
  print(data)
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)
  