from PM10_Class import PM_Reader
from NO2_Class import NO2_Reader
from O3_Class import O3_Reader
import time
import datetime


if __name__ == "__main__":
    while True:
        get_time = datetime.datetime.now()
        current_time = get_time.strftime("%Y-%m-%d %H:%M:%S")
        print("****************************************************")

        # acquire data of NO2 sensor
        no2Object = NO2_Reader()
        no2Response = no2Object.get_no2()
        if no2Response == 0:
            print("NO2 data is stored  ::  " + current_time)
        else:
            print(no2Response)

        # acquire data of O3 sensor
        o3object = O3_Reader()
        o3Response = o3object.get_o3()
        if o3Response == 0:
            print("O3 data is stored  ::  " + current_time)
        else:
            print(o3Response)

        # acquire data of PM10 sensor
        pmObject = PM_Reader()
        pmObject.openPort()
        pmResponse = pmObject.get_pm()
        if pmResponse == 0:
            print("PM10 data is stored  ::  " + current_time)
        else:
            print(pmResponse)
        pmObject.closePort()

        # TODO : talk to guys to choose a best time interval for data
        # the interval to acquire data from sensor
        time.sleep(60)