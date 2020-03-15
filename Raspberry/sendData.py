from DbClass import sqliteClass
import json
import requests
import datetime
import time

db = sqliteClass()


def readData():
    dataDF = db.select('sensors_data', '*', 'data_sent=0')
    return dataDF


def sendData(data):
    counting = 0
    for index, row in data.iterrows():
        data_id = row['data_id']
        sensorData = row['data_sensor_json']
        sensorName = row['data_sensor_name']
        sensorDate = row['data_date']

        jsonToSend = json.loads(sensorData)
        jsonToSend['data_sensor_name'] = sensorName
        jsonToSend['data_date'] = sensorDate
        try:
            rResponse = requests.post('http://indoorpi.local:8090/getdata', json=jsonToSend)
            if rResponse.text == 'status=ok':
                dResponse = db.update('sensors_data', 'data_sent=1', 'data_id=' + str(data_id))
                if dResponse == 0:
                    counting += 1
                else:
                    print 'error in updating status of data_id: ', data_id
            else:
                print 'error in sending data_id: ', data_id
        except requests.exceptions.ConnectionError as err:
            print err
            break
        except requests.exceptions.RequestException as err:
            print err
            break
    print 'From ', len(data), 'rows, ', counting, ' are sent successfully.'


def cleanDb():
    now = datetime.datetime.now()
    if now.hour == 0 and now.minute == 0:
        two_days = now - datetime.timedelta(days=2)
        rowcount = db.delete('sensors_data', 'data_date < \'' + str(two_days) + '\'')
        print str(rowcount), ' Rows are deleted.'


if '__main__' == __name__:
    while True:
        cleanDb()
        data = readData()
        print 'Total rows for send to IndoorPI ', len(data)
        sendData(data)
        time.sleep(60)


