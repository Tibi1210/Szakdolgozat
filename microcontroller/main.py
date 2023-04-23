def send_data(sensorAvg):
    try:
        ntptime.settime()  
    except:  
        time.sleep(1)
        send_data(sensorAvg)
    try:
        timeDiff=946681200
        timeStamp = time.mktime(time.localtime())+timeDiff
        insertJson = json.dumps({
            "collection": "plant1",
            "database": "plants",
            "dataSource": "Cluster0",
            "document": {
                "Timestamp": timeStamp, 
                "Light": round(sensorAvg[0]),
                "Temperature": sensorAvg[1],
                "Humidity": sensorAvg[2],
                "SoilMoisture": round(sensorAvg[3]),
                "delete": 1
            }
        })
        urequests.request("POST", insertUrl, headers=headers, data=insertJson)
        return insertJson
    except Exception as e:
        raise Exception("send_data(): "+str(e))

def analog_read_light():
    lightPin.on()
    soilPin.off()
    time.sleep(1)
    maxLight=950
    minLight=0
    lightValue = (analogPin.read() - minLight) / (maxLight - minLight) * 100
    return lightValue

def analog_read_soil():
    lightPin.off()
    soilPin.on()
    time.sleep(1)
    minMoisture=31551
    maxMoisture=9215
    soilMoisture = (analogPin.read_u16() - minMoisture) / (maxMoisture - minMoisture) * 100
    return soilMoisture

def measure_DHT():
    try:
        tempSensorPin.measure()
    except:
        time.sleep(1)
        measure_DHT()

def digial_read_temp():
    measure_DHT()
    sensorTemp = tempSensorPin.temperature()
    sensorHum = tempSensorPin.humidity()
    return [sensorTemp,sensorHum]

def avg_data(intervalValue):
    try:
        sampleSize=intervalValue*2
        scanInterval=round(86400/intervalValue/sampleSize)
        if scanInterval<1:
            scanInterval=1

        sumLight=sumTemp=sumSoil=sumHumid=0

        for i in range(sampleSize):
            tempValue, humValue = digial_read_temp()
            sumLight += analog_read_light()
            sumTemp += tempValue
            sumHumid += humValue
            sumSoil += analog_read_soil()
            time.sleep(scanInterval)

        avgLight=sumLight/sampleSize
        avgTemp=sumTemp/sampleSize
        avgHumid=sumHumid/sampleSize
        avgSoil=sumSoil/sampleSize

        return [avgLight,avgTemp,avgHumid,avgSoil]
    except Exception as e:
        raise Exception("avg_data(): "+str(e))

def waterpump_toggle(soilMoisture):
    if soilMoisture<30:
        relayPin.on()
        time.sleep(3)
        relayPin.off()

def get_settings():
    try:
        findData = json.dumps({
            "collection": "device1",
            "database": "devices",
            "dataSource": "Cluster0",
            "projection": {
                "_id": 0,
                "interval": 1,
                "pump": 1
            },
            "filter": {
            "_id": 1
            }
        })
        dataResponse = json.loads(urequests.request("POST", findOneUrl, headers=headers, data=findData).text)
        return dataResponse['document']['interval'],dataResponse['document']['pump']
    except Exception as e:
        raise Exception("get_settings(): "+str(e))





exceptionRaised=False
while not exceptionRaised:
    try:    
        scanInterval,pumpState=get_settings()

        sensorAvg=avg_data(scanInterval)  

        sentData=send_data(sensorAvg) 
        print(sentData)
        print()

        if pumpState:
            waterpump_toggle(sensorAvg[3])

    except Exception as e:
        relayPin.off()
        ledPin.off()
        exceptionRaised=True

        htmlPage = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>My MicroPython Web Server</title>
        </head>
        <body>
            <h1>MAIN</h1>
            <h2>"""+str(e)+"""</h2>
            <h2>Restart required</h2>
        </body>
        </html>
        """

        clientSocket, clientAddress = serverSocket.accept()
        serve(clientSocket,htmlPage)


        
    
