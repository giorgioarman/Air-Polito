import pandas as pd
import sqlite3
# import mysql.connector as mySQL
# from mysql.connector import Error
# from mysql.connector import errorcode
# from datetime import datetime

# direc = '/home/pi/Desktop/Project/OutdoorDB.db'
# direc ='IndoorDb.db'


class sqliteClass(object):
    def __init__(self, dirDB):
        self.dirDb = dirDB

    def connectDb(self):
        self.dbCon = sqlite3.connect(self.dirDb)

    def select(self, table, columns, where=None, orderBy=None, groupBy=None):
        try:
            self.connectDb()
            sqlQuery ="select "+ columns +" from " + table +\
                (" where " + where if where is not None else "") + \
                (" GROUP BY " + groupBy if groupBy is not None else "") + \
                (" ORDER BY " + orderBy if orderBy is not None else "")
            resultQuery = self.dbCon.execute(sqlQuery)
            cols = [column[0] for column in resultQuery.description]
            df = pd.DataFrame(resultQuery.fetchall(), columns=cols)
            self.dbCon.close()
            return df
        except sqlite3.Error as error:
            print("Failed to retrieve: {}".format(error))

    def insert(self, table, parameters, values):
        try:
            self.connectDb()
            sqlQuery = "INSERT INTO "+ table + " (" + parameters + ") VALUES (" + values + ")"
            self.dbCon.execute(sqlQuery)
            self.dbCon.commit()
            self.dbCon.close()
            # print("row is inserted")
            return 0

        except sqlite3.Error as error:
            return "Failed to insert, {}".format(error)

    def update(self, table, values, where=None):
        try:
            self.connectDb()
            sqlQuery = "UPDATE " + table + " SET " + values +\
                (" where " + where if where is not None else "")

            cur = self.dbCon.cursor()
            cur.execute(sqlQuery)
            self.dbCon.commit()
            self.dbCon.close()
            return 0

        except sqlite3.Error as error:
            return "Failed to update, {}".format(error)

    def delete(self, table, where=None):
        try:
            self.connectDb()
            sqlQuery = "select count(*) from " + table + \
                       (" where " + where if where is not None else "")
            rowCount = self.dbCon.execute(sqlQuery).fetchone()[0]
            sqlQuery = "DELETE from " + table + " WHERE " + where
            cur = self.dbCon.cursor()
            cur.execute(sqlQuery)
            self.dbCon.commit()
            self.dbCon.close()
            return rowCount

        except sqlite3.Error as error:
            return "Failed to delete, {}".format(error)

# ############      SAMPLE OF USING SQLITE      ##################################

# test = sqliteClass('OutdoorPi\IndoorDb.db')
# for i in range(10):
#     test.insert("sensors_data", "data_sensor_name,data_sensor_json", "'DHT222','temp="+str(20+i)+",hum="+str(80+i)+"'")
#
# xx = test.select("sensors_data", "*", "data_id >4")
# print xx

# class Mysql(object):
#     def __init__(self):
#         self.db = mySQL.connect(host="localhost",user="root",passwd="mysql",db="airpolitodb")
#
#     def select(self, table, columns, where=None):
#         try:
#             query ="select "+ columns +" from " + table +\
#                    (" where " + where if where is not None else "")
#             cur = self.db.cursor()
#             cur.execute(query)
#             df = pd.DataFrame(cur.fetchall())
#             df.columns = cur.column_names
#             cur.close()
#             return df
#         except mySQL.Error as error:
#             print("Failed to insert record into Laptop table {}".format(error))
#
#     def insert(self, table, parameters, values):
#         try:
#             cur = self.db.cursor()
#             sql = "INSERT INTO "+ table +" ("+parameters +") VALUES (" + values + ")"
#             cur.execute(sql)
#             self.db.commit()
#             cur.close()
#             print("row is inserted")
#         except mySQL.Error as error:
#             print("Failed to insert record into Laptop table {}".format(error))
# ############      SAMPLE OF USING MYSQL     ##################################
#
#     test = Mysql()
#     test.select("sensor_dht","*","ID >4")
#
#     test.insert("sensor_dht","datetime,temprature_value,humidity_value", "'" + str(datetime.now())+"',25,50")
#
#


