import pandas as pd 
import sqlalchemy


# pull the list of symbols from db or file 
class Symbol_map:
    # db connection consists of server 
    def __init__(self, feedType = None, fileName=None, filetype = None ,dbConnection=None, dbtype =None):

        if feedType == 'FILE':
            self.symbols =  self.get_list_from_file(self, fileName)
        if feedType == "DB":
            self.symbols = self.get_list_from_db(dbConnection, dbtype)

# grab the data from a database 
    def get_list_from_db(self, dbConnection, dbtype):
            
        if dbtype == "MSSQL":
            server, database = dbConnection
            engine = sqlalchemy.create_engine('mssql+pyodbc://@' + f'{server}' + '/' + f'{database}' + '?trusted_connection=yes&driver=ODBC Driver 17 for SQL Server')
            sql = ("SELECT * from symbols ")
            result  = pd.read_sql(sql, con= engine)
            return result
            
# grab the data from a file 
    def get_list_from_file(self,filename, filetype):
            if filetype =='csv':
                path = filename 
                df = pd.read_csv(path)
                return df
            elif filetype =="xls":
                path = filename
                df = pd.read_excel(path)
                return df 
            elif filetype =='json':
                path = filename
                df = pd.read_json
                return df       
# turn data into a list 
    def get_list(self, data):
        d = pd.DataFrame(data)
# return symbols
    def get_symbols(self):
        return self.symbols
    