# # import pymysql as mariadb
# # db = mariadb.connect(host="172.20.10.4",port=3306,user="root",passwd="mysql",db= "airpolitodb")
# # cursor = db.cursor()
# # cursor.execute("SELECT * FROM sensor_dht")
# # data = cursor.fetchone()
# # print ("Database version : %s " % data)
#
# import mysql.connector as mariadb
# db = mariadb.connect(host="172.20.10.4",port="3306",user="root",passwd="mysql",db= "airpolitodb")
# # #cursor = db.cursor()
# # #cursor.execute("SELECT * FROM sensor_dht")
# # #data = cursor.fetchone()
# # #print ("Database version : %s " % data)
# print("done")

sleep = 0
mode = 0 if sleep else 1
print(mode)