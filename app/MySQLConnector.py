import datetime

import mysql.connector
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine



class MySQLConnector:
    def __init__(self, conn):
        self.conn = conn
        self.sqlalachemyString='mysql+mysqlconnector://'+conn["user"]+":"+conn["password"]+"@"+conn["host"]+":"+conn["port"]+"/"+conn["db"]
        self.sqlalchemyArgs= {'ssl_ca':conn["CA_cert"]} if self.conn["CA_required"]== True else None

    def connect(self):
        return mysql.connector.connect(user=self.conn["user"], password=self.conn["password"], host=self.conn["host"],
                                                  port=self.conn["port"],database=self.conn["db"],
                                             ssl_ca=self.conn["CA_cert"] if self.conn["CA_required"]== True else None)

    def select(self,query):
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute(query)
        myresult = cursor.fetchall()
        cursor.close()
        connection.close()
        return myresult


    def insertDynTable(self, data, table):


        connection = self.connect()
        cursor = connection.cursor()

        executionTime=datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        query = "INSERT INTO " + table + "(codice,campo,valore,dataora)  VALUES (%s, %s, %s, %s)"
        values=[]
        data.reset_index(drop=True, inplace=True)
        for column in data:
            c=0
            for row in data[column]:
                if(str(row)!="nan"):
                    values.append((str(data["Codice"][c]),str(column),str(row),str(executionTime)))
                c+=1

        cursor.executemany(query, values)
        connection.commit()

        cursor.close()
        connection.close()

    def insertTable(self, data, table):

        engine = create_engine(self.sqlalachemyString, connect_args=self.sqlalchemyArgs, echo=False)
        data.to_sql(con=engine, name=table, if_exists='append', index=False)



