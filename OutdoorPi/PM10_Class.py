from __future__ import print_function
from serial import Serial
import struct, time, json
from DbClass import sqliteClass

db = sqliteClass('/home/pi/Desktop/Project/OutdoorDB.db')
DEBUG = 0
CMD_MODE = 2
CMD_QUERY_DATA = 4
CMD_DEVICE_ID = 5
CMD_SLEEP = 6
CMD_FIRMWARE = 7
CMD_WORKING_PERIOD = 8
MODE_ACTIVE = 0
MODE_QUERY = 1
TRYFLAG = 0
JSON_FILE = '/var/www/html/aqi.json'
byte, data = 0, ""
portName = "/dev/ttyUSB0"
#portName = "COM4"


class PM_Reader(object):
    def __init__(self):
        try:
            Serial(port=portName, baudrate=9600).close()
            self.ser = Serial(port=portName, baudrate=9600, timeout=1)
            time.sleep(0.2)
        except:
            self.ser = Serial(port=portName, baudrate=9600, timeout=1)

    def openPort(self):
        if self.ser.is_open:
            self.ser.flushInput()
        else:
            self.ser.open()
            self.ser.flushInput()

    def closePort(self):
        self.ser.close()

    def construct_command(self, cmd, data=[]):
        assert len(data) <= 12
        data += [0, ] * (12 - len(data))
        checksum = (sum(data) + cmd - 2) % 256
        ret = "\xaa\xb4" + chr(cmd)
        ret += ''.join(chr(x) for x in data)
        ret += "\xff\xff" + chr(checksum) + "\xab"
        return ret

    def process_data(self, d):
        r = struct.unpack('<HHxxBB', d[2:])
        pm25 = r[0] / 10.0
        pm10 = r[1] / 10.0
        checksum = sum(ord(v) for v in d[2:8]) % 256
        return [pm25, pm10]

    def read_response(self):
        byte = 0
        while byte != "\xaa":
            byte = self.ser.read(size=1)

        d = self.ser.read(size=9)
        return byte + d

    def cmd_set_mode(self, mode=MODE_QUERY):
        self.ser.write(self.construct_command(CMD_MODE, [0x1, mode]))
        self.read_response()

    def cmd_query_data(self):
        self.ser.write(self.construct_command(CMD_QUERY_DATA))
        d = self.read_response()
        values = []
        if d[1] == "\xc0":
            values = self.process_data(d)
        return values

    def cmd_set_sleep(self, sleep):
        mode = 0 if sleep else 1
        self.ser.write(self.construct_command(CMD_SLEEP, [0x1, mode]))
        self.read_response()

    def get_pm(self):
        # print("checkpoint1")
        self.cmd_set_sleep(0)
        time.sleep(0.2)
        self.cmd_set_mode(1)
        print("Sensor is ON (Waiting for 5 Sec to get valid measurement)")
        time.sleep(5)

        for t in range(4):
            values = self.cmd_query_data()
            if values is not None and len(values) == 2:
                print("attempt no."+str(t) + " : PM2.5: ", values[0], ", PM10: ", values[1])
                time.sleep(2)
        cResult = -1
        if values is not None and len(values) == 2:
            outputJson = json.dumps({'pm25': values[0], 'pm10': values[1]})
            print(outputJson)
            cResult = db.insert("sensors_data", "data_sensor_name,data_sensor_json",
                                    "'PM10','" + str(outputJson) + "'")
        try:
            if self.ser.is_open:
                self.cmd_set_mode(0)
                time.sleep(0.2)
                self.cmd_set_sleep(1)
                self.closePort()
            else:
                self.openPort()
                self.cmd_set_mode(0)
                time.sleep(0.2)
                self.cmd_set_sleep(1)
                self.closePort()
        except:
            self.openPort()
            self.cmd_set_sleep(0)
            time.sleep(0.2)
            self.cmd_set_sleep(1)
            self.closePort()
        return cResult