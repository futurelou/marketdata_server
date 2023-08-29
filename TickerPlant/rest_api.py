from flask import Flask
from flask_restful import Resource, Api, abort, reqparse
import threading 
from yahoo_handler import Yahoo_handler
from store import Storage
from symbols import Symbol_map
import queue 
q = queue.Queue()
import configparser
config = configparser.RawConfigParser()

configFilePath = r'C:\Users\louie\crypto_trade\config.cfg'
config.read(configFilePath)

app = Flask(__name__)
api = Api(app)


parser = reqparse.RequestParser()
parser.add_argument('Source')
parser.add_argument('Storage_file_type')
parser.add_argument('Db_connection')
parser.add_argument('feedtype')
parser.add_argument('filename')

is_storage_running = False 

feeds = {
    'yahoofeed': {'Source': 'Yahoo_finance', 'Storage_file_type': 'csv', 'Db_connection': ['LOUIS-PC', 'Crypto_market_prices', 'MSSQL'], 'feedtype': 'DB', 'filename': '1_hour_interval_crypto_data'}



 }

def abort_if_feed_dosent_exist(feedid):
    if feedid not in feeds:
        abort(404, message = f'{feedid} is not running')


class Feed(Resource):

    def get(self,feedid):
        abort_if_feed_dosent_exist(feedid)
        return feeds[feedid]
    
    def stop(self,feedid):
        abort_if_feed_dosent_exist(feedid)
        feedid.stop()
        

    def run(self,feedid): 
        abort_if_feed_dosent_exist(feedid)    

        y = Symbol_map(feedType=feedid['feedtype'], dbConnection=(feedid['Db_connection'][0], feedid['Db_connection'][1]), dbtype=feedid['Db_connection'][2])
        params = (config['FILEPATH']['Crypto_Data'], feedid['filename'])

        format_source = ''.join([i for i in feedid['Source'] if not i.isdigit()])

        if format_source == "Yahoo_finance":
            z = Storage(q,feedid['Storage_file_type'])
            threading.Thread(target=z.run,daemon=True, args=(params,)).start()
            feedid = Yahoo_handler(Q=q, symbols=y)
            threading.Thread(target=feedid.run,daemon=True).start()

        if feedid['Source'] == "Yahoo_finance":
            pass

    def put(self, feedid):
        args = args.parser
        Source = {'Source':args['Source']}
        Storage_file_type = {'Storage_file_type': args['Storage_file_type']}
        Db_connection = {'Db_connection': [args[0],args[1], args[2]]}
        feedtype = {'feedtype':args['feedtype']}
        filename = {'filename':args['filename']}

        feedid['Source'] = Source
        feedid['Storage_file_type'] = Storage_file_type
        feedid['Db_connection'] = Db_connection
        feedid['feedtype'] = feedtype
        feedid['filename'] = filename

        return Source, Storage_file_type, Db_connection, feedtype, filename
    
class FeedList(Resource):
    def get(self):
        return feeds

    def post(self, feed):
        args = parser.parse_args()
        feedid = int(max(feeds.keys()).lstrip(feed)) + 1
        feedid = 'todo%i' % feedid
        feeds[feedid] = {'Source':args['Source'], 'Storage_file_type': args['Storage_file_type'], 'Db_connection': [args[0],args[1], args[2]],'feedtype':args['feedtype','filename':args['filename']]}
        return feeds[feedid], 201
        

api.add_resource(Feed, '/feeds/<feedid>')
api.add_resource(FeedList,'/feeds')
        

            

if __name__ == '__main__':
    app.run(debug=True)

