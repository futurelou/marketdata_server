import queue
import pyodbc
import pandas as pd
import sqlalchemy

class Storage:
    def __init__(self, Q):
        self.q = Q

    def take_off_q(self):
        data = self.q.get(block = False, timeout = None)
        return data

    def save_to_csv(self,path,filename):
        filepath = path + filename
        data = self.take_off_q()
        data.to_csv(filepath)
         
    def save_to_db(self,server,database):
        engine = sqlalchemy.create_engine('mssql+pyodbc://@' + f'{server}' + '/' + f'{database}' + '?trusted_connection=yes&driver=ODBC Driver 17 for SQL Server')
        data = self.take_off_q()
        data.to_sql(f'{database}', engine,if_exists='append')


    









