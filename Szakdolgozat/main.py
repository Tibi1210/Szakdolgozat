def send_data(values):
    try:
        ntptime.settime()  
    except:
        send_data(values)

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
            "SoilMoisture": values[3]
        }
    })
    #urequests.request("POST", insertUrl, headers=headers, data=insert)
    return insert

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

def digial_read_temp():
    temp = temp1.temperature()
    hum = temp1.humidity()
    return [temp,hum]

def avg_data(samplesize,interval):
    sum_light=0
    sum_temp=0
    sum_soil=0
    sum_humid=0

    i=0
    while i<samplesize:
        temp1.measure()
        sum_light += analog_read_light()
        sum_temp += digial_read_temp()[0]
        sum_humid += digial_read_temp()[1]
        sum_soil += analog_read_soil()
        time.sleep(interval)
        i+=1

    i=0
    avg_light=sum_light/samplesize
    avg_temp=sum_temp/samplesize
    avg_humid=sum_humid/samplesize
    avg_soil=sum_soil/samplesize

    return [avg_light,avg_temp,avg_humid,avg_soil]

def waterpump_toggle(moisture):
    if moisture<10:
            relay1.on()
            time.sleep(3)
            relay1.off()

hiba=False
while not hiba:
    try:
        #20 minta 30s-enként = 10perc
        avg=avg_data(5,1)
        send=send_data(avg)
        print(send)
        print()
        waterpump_toggle(avg[3])
        

    except Exception as e:
        relay1.off()
        print(e)
        led.off()
        hiba=True  
    
