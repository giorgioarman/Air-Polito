"Reading Data of Temperature and Humidity"
import Adafruit_DHT
from DbClass import sqliteClass
import datetime
import json
import time


class DHT11_Reader(object):
    def __init__(self):
        self.humidity = 0
        self.temperature = 0
        self.flagPrint = False

    def sensorData(self):
        sensor_type = Adafruit_DHT.AM2302
        try:
            self.humidity, self.temperature = Adafruit_DHT.read_retry(sensor_type, 19)
            "Reading Data of sensor DHT11 on PIN 19 of Raspberry"
        except:
            return 'Temp_Humidity_Sensor: ERROR IN READING THE SENSOR'

        if self.humidity != 0 and self.temperature != 0:
            if self.flagPrint:
                get_time = datetime.datetime.now()
                current_time = get_time.strftime("%Y-%m-%d %H:%M:%S")
                print("Temp_Humidity_Sensor : ", 'Time: ', current_time,
                      'Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(self.temperature, self.humidity))
                self.flagPrint = False
            "put all the data in a Json"
            OutputJson = json.dumps({"temperature": round(self.temperature, 2), "humidity": round(self.humidity, 2)})
            sqlite = sqliteClass()
            cResult = sqlite.insert("sensors_data", "data_sensor_name,data_sensor_json",
                        "'DHT222','"+str(OutputJson)+"'")
            return cResult
        else:
            return 'Temp_Humidity_Sensor: ERROR IN SENDING JSON'


if __name__ == '__main__':
    "this is for testing we use this class in the PublishTempHum class"
    dhtClass = DHT11_Reader()
    dhtClass.flagPrint = True
    counter = 0
    while True:
        if counter > 10:
            dhtClass.flagPrint = True
            counter = 0
        sData = dhtClass.sensorData()
        if sData != 0:
            print(sData)
        counter += 1
        time.sleep(30)
