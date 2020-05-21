import datetime
import random
import struct, time, json
from DbClass import sqliteClass
import time
import Adafruit_ADS1x15

db = sqliteClass('/home/pi/Desktop/Project/OutdoorDB.db')
# db = sqliteClass('OutdoorDB.db')
#

class NO2_Reader(object):
    # TODO: must connect sensor to the class and remove random number

    def get_no2(self):
        adc = Adafruit_ADS1x15.ADS1115()
        GAIN = 1
        value = 0
        maxVoltage=4.096
        maxBitadc=32767
        R0=800
        Rload=22000
        Involtage=5
        value = adc.read_adc(0, gain=GAIN)
        voltage=(maxVoltage*value)/maxBitadc
        Rsensor=Rload*((Involtage/voltage)-1)
        no2Valueppb=Rsensor/R0
        no2Value=no2Valueppb*1.88
        
        cResult = -1
        if no2Value is not None:
            outputJson = json.dumps({'no2': no2Value})
            print(outputJson)
            cResult = db.insert("sensors_data", "data_sensor_name,data_sensor_json",
                                    "'NO2','" + str(outputJson) + "'")

        return cResult
