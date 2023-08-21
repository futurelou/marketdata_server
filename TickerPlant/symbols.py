import pandas as pd 
import sqlalchemy


class Symbol_map:
    # db connection consists of server 
    def __init__(self, feedType = None, fileName=None, filetype = None ,dbConnection=None, dbtype =None):

        if feedType == 'FILE':
            self.symbols =  self.get_list_from_file(self, fileName)
        if feedType == "DB":
            self.symbols = self.get_list_from_db(dbConnection, dbtype)


    def get_list_from_db(self, dbConnection, dbtype):
            
        if dbtype == "MSSQL":
            server, database = dbConnection
            engine = sqlalchemy.create_engine('mssql+pyodbc://@' + f'{server}' + '/' + f'{database}' + '?trusted_connection=yes&driver=ODBC Driver 17 for SQL Server')
            sql = ("SELECT * from symbols ")
            result  = pd.read_sql(sql, con= engine)
            return result
            

    def get_list_from_file(self,fileName, filetype):
        pass 

    def get_list(self, data):
        d = pd.DataFrame(data)

    def get_symbols(self):
        return self.symbols
    