from PM10_Class import PM_Reader
import time


if __name__ == "__main__":
    while True:
        pmObject = PM_Reader()
        pmObject.openPort()
        pmValue = pmObject.get_pm()
        if pmValue == 0:
            print("Data is stored" + "\n" + "wait for next data acquisition in 60 Sec")
        pmObject.closePort()
        time.sleep(60)