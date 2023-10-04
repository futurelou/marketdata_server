import queue
import pyodbc
import pandas as pd
import sqlalchemy
import time

# used to store data into different formats in near real time
class Storage:
    def __init__(self, Q, savetype):
        self.q = Q
        self.started = False      
        self.savetype = savetype
        
# is storage running 
    def start(self):
        self.started = True
# has sotrage stopped running 
    def stop(self):
        self.started = False
# start running storage 
    def run(self, params):
        self.start()
        while self.started:
            if self.savetype == 'DB':
                server , database, table_name = params
                self.save_to_db(server,database, table_name)
            elif self.savetype =='csv':
                path , filename = params
                self.save_to_csv(path,filename)
                
            
# pull data off of the queue 
# the queue is looking for data constantly 
    def take_off_q(self):
        while self.q.empty():
            time.sleep(2)
            
        data = self.q.get(block = False, timeout = None)
        return data
# save the data to csv if choose to do so 
    def save_to_csv(self,path,filename):
        filepath = path + filename
        data = self.take_off_q()
        data.to_csv(filepath, mode = 'a')
# save to a db if choose to do so      
    def save_to_db(self,server,database, table_name):
        engine = sqlalchemy.create_engine('mssql+pyodbc://@' + f'{server}' + '/' + f'{database}' + '?trusted_connection=yes&driver=ODBC Driver 17 for SQL Server')
        data = self.take_off_q()
        data.to_sql(f'{table_name}', engine,if_exists='append')


    









