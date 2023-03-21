def send_data(values):
    try:
        ntptime.settime()  
    except:  
        time.sleep(1)
        send_data(values)
    try:
        timedifference=946681200
        timestamp = time.mktime(time.localtime())+timedifference
        insert = json.dumps({
            "collection": "plant1",
            "database": "plants",
            "dataSource": "Cluster0",
            "document": {
                "Timestamp": timestamp, 
                "Light": values[0],
                "Temperature": values[1],
                "Humidity": values[2],
                "SoilMoisture": values[3],
                "delete": 1
            }
        })
        urequests.request("POST", insertUrl, headers=headers, data=insert)
        return insert
    except Exception as e:
        raise Exception("send_data(): "+str(e))

def analog_read_light():
    light1.on()
    soil1.off()
    time.sleep(1)
    max_light=950
    min_light=0
    light = (analog.read() - min_light) / (max_light - min_light) * 100
    return light

def analog_read_soil():
    light1.off()
    soil1.on()
    time.sleep(1)
    min_moisture=31551
    max_moisture=9215
    moisture = (analog.read_u16() - min_moisture) / (max_moisture - min_moisture) * 100
    return moisture

def measureDHT():
    try:
        temp1.measure()
    except:
        time.sleep(1)
        measureDHT()

def digial_read_temp():
    measureDHT()
    temp = temp1.temperature()
    hum = temp1.humidity()
    return [temp,hum]

def avg_data(value):
    try:
        samplesize=value*2
        interval=round(86400/value/samplesize)
        if interval<1:
            interval=1

        sum_light=0
        sum_temp=0
        sum_soil=0
        sum_humid=0

        i=0
        samplesize=5
        interval=1
        while i<samplesize:
            temp,hum=digial_read_temp()

            sum_light += analog_read_light()
            sum_temp += temp
            sum_humid += hum
            sum_soil += analog_read_soil()
            time.sleep(interval)
            i+=1

        i=0
        avg_light=sum_light/samplesize
        avg_temp=sum_temp/samplesize
        avg_humid=sum_humid/samplesize
        avg_soil=sum_soil/samplesize

        return [avg_light,avg_temp,avg_humid,avg_soil]
    except Exception as e:
        raise Exception("avg_data(): "+str(e))

def waterpump_toggle(moisture):
    if moisture<10:
            relay1.on()
            time.sleep(3)
            relay1.off()

def get_interval():
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
        return dataResponse['document']['interval']
    except Exception as e:
        raise Exception("get_interval(): "+str(e))





hiba=False
while not hiba:
    try:    
        interval=get_interval()

        avg=avg_data(interval)  

        send=send_data(avg) 
        print(send)
        print()

        #waterpump_toggle(avg[3])

    except Exception as e:
        relay1.off()
        led.off()
        hiba=True

        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>My MicroPython Web Server</title>
        </head>
        <body>
            <h1>MAIN</h1>
            <h2>"""+str(e)+"""</h2>
        </body>
        </html>
        """

        client_sock, client_addr = server_sock.accept()
        serve(client_sock,html)


        
    
