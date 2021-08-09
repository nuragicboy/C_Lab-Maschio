import datetime

import mysql.connector


class MySQLConnector:
    def __init__(self, conn):
        self.conn = conn



    def insertTable(self, data, table):

        connection = mysql.connector.connect(user=self.conn["user"], password=self.conn["password"], host=self.conn["host"],
                                                  port=self.conn["port"],database=self.conn["db"])
        cursor = connection.cursor()

        query = "INSERT INTO " + table + " VALUES (%s, %s, %s,\"" + datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S') +"\")"
        values=[]
        for column in data:
            c=0
            for row in data[column]:
                values.append((str(data["Codice"][c]),str(column),str(row) if str(row)!="nan" else ""))
                #query += "insert into " + table + " values (\"" + str(data["Codice"][c]) + "\",\"" + str(column) + "\"," + ("\""+str(
                #    row)+"\"" if str(row)!="nan" else "\"\"") + "," + now.strftime('%Y-%m-%d %H:%M:%S') + ");\n"
                c+=1
        #print(query)

        cursor.executemany(query, values)
        connection.commit()

        cursor.close()
        connection.close()


