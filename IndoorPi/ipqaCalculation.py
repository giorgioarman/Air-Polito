# coding=utf-8
from DbClass import sqliteClass
import json
import requests
import pandas as pd
import datetime
import time
import pandas

db = sqliteClass('/home/pi/Desktop/Project/IndoorDb.db')

# db = sqliteClass('IndoorDb.db')

# reference value (50µg/m3)
pmReference = 50
# reference value (200µg/m3)
no2Reference = 200
# reference value (120µg/m3)
o3Reference = 120


def readData():
    dataDF = db.select('sensors_data', '*, MAX(data_date) AS collectDate',
                       where='data_used=0',
                       groupBy='data_sensor_name',
                       orderBy='collectDate DESC ')
    return dataDF


def validationData(data):
    if len(data) == 4:
        current_time = datetime.datetime.now()

        pm10Time = datetime.datetime.strptime(
            data.loc[data['data_sensor_name'] == 'PM10']['data_date'].astype(str).values[0],
            "%Y-%m-%d %H:%M:%S")
        no2Time = datetime.datetime.strptime(data.loc[data['data_sensor_name'] == 'NO2']['data_date'].astype(str).values[0],
                                             "%Y-%m-%d %H:%M:%S")
        o3Time = datetime.datetime.strptime(data.loc[data['data_sensor_name'] == 'O3']['data_date'].astype(str).values[0],
                                            "%Y-%m-%d %H:%M:%S")

        minTime = min([pm10Time, no2Time, o3Time])
        maxTime = max([pm10Time, no2Time, o3Time])
        diffMaxMin = (maxTime - minTime).seconds / 60

        # TODO : discuss with guys to choose how much time between the collected data are acceptable
        # TODO : how many minute is acceptable after the data is collected ?
        if diffMaxMin < 3:
            diffMinCur = (minTime - current_time).seconds / 60
            if diffMinCur < 5000:
                return 'OK', minTime
            else:
                return 'The last received data are old'
        else:
            return 'Time between collected data from sensors are too much'

    else:
        return 'There is no data', ''


def applySurvey(pmValue, no2Value, o3Value):
    df = pd.read_csv("/home/pi/Desktop/Project/Abitudini.csv", header=0)
    output = 0
    for index, row in df.iterrows():
        date, primo, secondo, terzo, quarto, quinto = row
        output = 0
        if primo == 'Si':
            output += 3

        if secondo == 'Si':
            output += 2
        if secondo == 'A volte':
            output += 1

        if terzo == 'Vetro':
            output += 1

        if quarto == 'la apro solo quando necessario':
            output += 2
        elif quarto == 'a volte la lascio scorrere altre volte la chiudo':
            output += 1

        if quinto == 'Si':
            output += 2
        elif quinto == 'A volte':
            output += 1

    media = round(output / (len(df) - 1), 0)

    if media == 0 or media == 10:
        coefficient = 0.25
        if media == 10:
            coefficient *= -1
    if media == 1 or media == 9:
        coefficient = 0.20
        if media == 9:
            coefficient *= -1
    if media == 2 or media == 8:
        coefficient = 0.15
        if media == 8:
            coefficient *= -1
    if media == 3 or media == 7:
        coefficient = 0.10
        if media == 7:
            coefficient *= -1
    if media == 4 or media == 6:
        coefficient = 0.05
        if media == 6:
            coefficient *= -1

    pmValue += (pmValue * coefficient)
    no2Value += (no2Value * coefficient)
    o3Value += (o3Value * coefficient)

    return pmValue, no2Value, o3Value


def calculation(data, sensorDate):
    # Temp and Humidity
    dhtJson = json.loads(data.loc[data['data_sensor_name'] == 'DHT222']['data_sensor_json'].astype(str).values[0])
    temp = dhtJson['temperature']
    humi = dhtJson['humidity']

    # real value collected from sensors
    pmJson = json.loads(data.loc[data['data_sensor_name'] == 'PM10']['data_sensor_json'].astype(str).values[0])
    pm10Value = pmJson['pm10']
    pm25Value = pmJson['pm25']
    no2Value = json.loads(data.loc[data['data_sensor_name'] == 'NO2']['data_sensor_json'].astype(str).values[0])['no2']
    o3Value = json.loads(data.loc[data['data_sensor_name'] == 'O3']['data_sensor_json'].astype(str).values[0])['o3']

    #to apply result of servey in status
    pmValue, no2Value, o3Value = applySurvey(pm10Value, no2Value, o3Value)

    #Create JSON file to store in Database
    sensorsData = {'pm10': pm10Value, 'pm25': pm25Value, 'no2': no2Value, 'o3': o3Value, 'temp': temp, 'hum': humi}
    sensorsDataJson = json.dumps(sensorsData)

    # normalise value
    pm = int((pm10Value / float(pmReference)) * 100)
    no2 = int((no2Value / float(no2Reference)) * 100)
    o3 = int((o3Value / float(o3Reference)) * 100)

    # IPQA value and AIR Quality status
    ipqaValue = max(pm, no2, o3)

    if ipqaValue <= 0:
        raise KeyError("* PROBLEM CALCULATING IPQA *")
    elif ipqaValue > 0 and ipqaValue <= 50:
        ipqaStatus = "Ottima"
    elif ipqaValue > 50 and ipqaValue <= 70:
        ipqaStatus = "Buona"
    elif ipqaValue > 70 and ipqaValue <= 100:
        ipqaStatus = "Accettabile"
    elif ipqaValue > 100 and ipqaValue <= 200:
        ipqaStatus = "Cattiva"
    else:
        ipqaStatus = "Pessima"
    print ('APQI value is equal to: ', ipqaValue, ' and the status is: ', ipqaStatus, ' (at: ', sensorDate, ")")

    cResult = db.insert("apqi_data",
                        "apqi_value,apqi_status,sensor_json,date_sensors",
                        str(ipqaValue) + ",'" +
                        str(ipqaStatus) + "','" +
                        str(sensorsDataJson) + "','" +
                        str(sensorDate) + "'")
    if cResult == 0:
        dResponse = db.update('sensors_data', 'data_used=1')
        if dResponse == 0:
            return 'status=ok'
        else:
            return 'error in updating status of data'
    else:
        return 'status=error in inserting data'


def cleanDb():
    now = datetime.datetime.now()
    if now.hour == 0 and now.minute == 0:
        two_days = now - datetime.timedelta(days=7)
        rowcount = db.delete('sensors_data', 'data_date < \'' + str(two_days) + '\'')
        print(str(rowcount), ' Rows are deleted.')


if '__main__' == __name__:
    while True:
        get_time = datetime.datetime.now()
        current_time = get_time.strftime("%Y-%m-%d %H:%M:%S")
        print("***IPQA Calculation*******************************************" + current_time)
        cleanDb()
        data = readData()
        cVal, sensorDate = validationData(data)
        if cVal == 'OK':
            cResponse = calculation(data, sensorDate=sensorDate)
            if cResponse == 'status=ok':
                print('Data was inserted and table was updated successfully ')
            else:
                print(cResponse)
        else:
            print (cVal)
        time.sleep(10)
