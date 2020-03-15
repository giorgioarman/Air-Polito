from PM10_Class import PM_Reader
import time


if __name__ == "__main__":
    while True:
        pmObject = PM_Reader()
        pmObject.openPort()
        pmResponse = pmObject.get_pm()
        if pmResponse == 0:
            print("Data is stored" + "\n" + "wait for next data acquisition in 60 Sec")
        else:
            print(pmResponse)
        pmObject.closePort()
        time.sleep(60)