import pandas as pd
import sqlite3





class Mysql(object):
    def __init__(self):
        self.db = sqlite3.connect('test.db')


    def select(self, table, columns, where=None):
        try:
            query ="select "+ columns +" from " + table +\
                   (" where " + where if where is not None else "")
            cur = self.db.cursor()
            cur.execute(query)
            df = pd.DataFrame(cur.fetchall())
            df.columns = cur.column_names
            cur.close()
            return df
        except mySQL.Error as error:
            print("Failed to insert record into Laptop table {}".format(error))

    def insert(self, table, parameters, values):
        try:
            cur = self.db.cursor()
            sql = "INSERT INTO "+ table +" ("+parameters +") VALUES (" + values + ")"
            cur.execute(sql)
            self.db.commit()
            cur.close()
            print("row is inserted")
        except mySQL.Error as error:
            print("Failed to insert record into Laptop table {}".format(error))


# ############      SAMPLE OF USING       ##################################
#
#     test = Mysql()
#     test.select("sensor_dht","*","ID >4")
#
#     test.insert("sensor_dht","datetime,temprature_value,humidity_value", "'" + str(datetime.now())+"',25,50")
#
#


