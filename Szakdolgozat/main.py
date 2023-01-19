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
    urequests.request("POST", insertUrl, headers=headers, data=insert)
    return insert

def analog_read_light():
    light1.on()
    soil1.off()
    max_light=150
    min_light=950
    light = (max_light-analog.read())*100/(max_light-min_light)
    return light

def analog_read_soil():
    light1.off()
    soil1.on()
    max_moisture=31231
    min_moisture=9599
    moisture = (max_moisture-analog.read_u16())*100/(max_moisture-min_moisture)
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
        #print(i)
        time.sleep(interval)
        i+=1

    i=0
    avg_light=sum_light/samplesize
    avg_temp=sum_temp/samplesize
    avg_humid=sum_humid/samplesize
    avg_soil=sum_soil/samplesize

    return [avg_light,avg_temp,avg_humid,avg_soil]

hiba=False
while not hiba:
    try:
        #20 minta 30s-enként = 10perc
        send=send_data(avg_data(5,1))
        print(send)
        print()
          
    except Exception as e:
        print(e)
        led.off()
        hiba=True  
    
