from PM10_Class import PM_Reader
import time
import datetime


if __name__ == "__main__":
    while True:
        get_time = datetime.datetime.now()
        current_time = get_time.strftime("%Y-%m-%d %H:%M:%S")
        print("****************************************************")
        pmObject = PM_Reader()
        pmObject.openPort()
        pmResponse = pmObject.get_pm()
        if pmResponse == 0:
            print("Data is stored  ::  " + current_time)
        else:
            print(pmResponse)
        pmObject.closePort()
        time.sleep(60)