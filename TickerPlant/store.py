import queue
import pyodbc
import pandas as pd
import sqlalchemy
import time

class Storage:
    def __init__(self, Q, savetype):
        self.q = Q
        self.started = False 
        
        self.savetype = savetype

    def start(self):
        self.started = True

    def stop(self):
        self.started = False

    def run(self, params):
        self.start()
        while self.started:
            if self.savetype == 'DB':
                server , database, table_name = params
                self.save_to_db(server,database, table_name)
            elif self.savetype =='csv':
                path , filename = params
                self.save_to_csv(path,filename)
                
            

    def take_off_q(self):
        while self.q.empty():
            time.sleep(2)
            
        data = self.q.get(block = False, timeout = None)
        return data

    def save_to_csv(self,path,filename):
        filepath = path + filename
        data = self.take_off_q()
        data.to_csv(filepath, mode = 'a')
         
    def save_to_db(self,server,database, table_name):
        engine = sqlalchemy.create_engine('mssql+pyodbc://@' + f'{server}' + '/' + f'{database}' + '?trusted_connection=yes&driver=ODBC Driver 17 for SQL Server')
        data = self.take_off_q()
        data.to_sql(f'{table_name}', engine,if_exists='append')


    









