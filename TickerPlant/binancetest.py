import configparser
from binance.spot import Spot as Client

config = configparser.RawConfigParser()
configFilePath = r'C:\Users\louie\crypto_trade\config.cfg'
config.read(configFilePath)

client = Client(config['BIANANCE']['api_key'],config['BIANANCE']['secret_key'])


p = client.get_oco_order()