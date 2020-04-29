from DbClass import sqliteClass
import json
import requests
import datetime
import time

# db = sqliteClass('/home/pi/Desktop/Project/IndoorDb.db')
db = sqliteClass('IndoorDb.db')

urlRest = 'https://www.airpolito.it/restaqi-insert/'


def readData():
    dataDF = db.select('apqi_data', '*', 'data_sent=0', limit=20)
    return dataDF


def sendData(data):
    counting = 0
    cError = None
    for index, row in data.iterrows():

        data_id = row['data_id']
        apqi_value = row['apqi_value']
        apqi_status = row['apqi_status']
        sensor_json = row['sensor_json']
        date_sensors = row['date_sensors']

        jsonToSend = {}
        jsonToSend['aqi_status'] = apqi_status
        jsonToSend['aqi_value'] = apqi_value
        jsonToSend['aqi_sensor_data'] = sensor_json
        jsonToSend['aqi_date_collect'] = date_sensors
        try:
            rResponse = requests.post(urlRest, json=jsonToSend, auth=('arman', 'okAbc1234'))
            rrResponse = json.loads(rResponse.text)
            if rrResponse['message'] == 'AQI was Inserted.':
                dResponse = db.update('apqi_data', 'data_sent=1', 'data_id=' + str(data_id))
                if dResponse == 0:
                    counting += 1
                else:
                    cError = 'error in updating status of data_id: ', data_id
            else:
                cError = 'error in sending data_id: ', data_id
        except requests.exceptions.ConnectionError as err:
            cError = err
            break
        except requests.exceptions.RequestException as err:
            cError = err
            break
        except:
            dResponse = db.update('apqi_data', 'data_sent=1', 'data_id=' + str(data_id))
            cError = 'error in rendering response from server'

    if cError is None:
        return "From {0} rows, {1} are sent successfully.".format(len(data), counting)
    else:
        return cError


def cleanDb():
    now = datetime.datetime.now()
    if now.hour == 0 and now.minute == 0:
        two_days = now - datetime.timedelta(days=10)
        rowcount = db.delete('apqi_data', 'date_sensors < \'' + str(two_days) + '\'')
        print (str(rowcount), ' Rows are deleted.')


if '__main__' == __name__:
    while True:
        get_time = datetime.datetime.now()
        current_time = get_time.strftime("%Y-%m-%d %H:%M:%S")
        print("*****Send to Online DB***********************************" + current_time)
        cleanDb()
        data = readData()
        if len(data) > 0:
            print ('Total rows for sending to OnLine Database ', len(data))
            sdResponse = sendData(data)
            print (sdResponse)
        time.sleep(10)


