import datetime
import random
import struct, time, json
from DbClass import sqliteClass

db = sqliteClass('/home/pi/Desktop/Project/OutdoorDB.db')


class O3_Reader(object):
    # TODO: must connect sensor to the class and remove random number

    def get_o3(self):
        o3Value = random.randrange(90, 150)
        cResult = -1
        if o3Value is not None:
            outputJson = json.dumps({'o3': o3Value})
            print(outputJson)
            cResult = db.insert("sensors_data", "data_sensor_name,data_sensor_json",
                                    "'O3','" + str(outputJson) + "'")

        return cResult