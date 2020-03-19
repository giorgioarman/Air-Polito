import datetime
import random
import struct, time, json
from DbClass import sqliteClass

db = sqliteClass('/home/pi/Desktop/Project/OutdoorDB.db')
# db = sqliteClass('OutdoorDB.db')
#

class NO2_Reader(object):
    # TODO: must connect sensor to the class and remove random number

    def get_no2(self):
        no2Value = random.randrange(90, 250)
        cResult = -1
        if no2Value is not None:
            outputJson = json.dumps({'no2': no2Value})
            print(outputJson)
            cResult = db.insert("sensors_data", "data_sensor_name,data_sensor_json",
                                    "'NO2','" + str(outputJson) + "'")

        return cResult