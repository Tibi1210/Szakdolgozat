try:
  import usocket as socket
except:
  import socket

from machine import Pin, ADC
import network
import ntptime
import time
import urequests
import ujson as json
import dht

analogPin = ADC(0)
lightPin = Pin(0, Pin.OUT)
soilPin = Pin(14, Pin.OUT)
ledPin = Pin(2, Pin.OUT)
tempSensorPin = dht.DHT11(Pin(5))
relayPin = Pin(4, Pin.OUT)
relayPin.off()
ledPin.off()

insertUrl = "https://data.mongodb-api.com/app/data-ojsvg/endpoint/data/v1/action/insertOne"
findOneUrl = "https://data.mongodb-api.com/app/data-ojsvg/endpoint/data/v1/action/findOne"

api=""

ssid = ''
password = ''


headers = {
  'Content-Type': 'application/json',
  'Access-Control-Request-Headers': '*',
  'api-key': api, 
}


wlanStation = network.WLAN(network.STA_IF)
wlanStation.active(True)
wlanStation.connect(ssid, password)
accessPoint = network.WLAN(network.AP_IF)
accessPoint.active(False)

while wlanStation.isconnected() == False:
  pass

def begin_settime():
  try:
    ntptime.host = "1.europe.pool.ntp.org"
    ntptime.settime()
  except Exception as e:
    htmlPage = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>My MicroPython Web Server</title>
        </head>
        <body>
            <h1>BOOT</h1>
            <h2>"""+str(e)+"""</h2>
            <h2>Restart required</h2>
        </body>
        </html>
        """

    clientSocket, clientAddress = serverSocket.accept()
    serve(clientSocket,htmlPage)

def serve(clientSocket,htmlPage):
    request = clientSocket.recv(1024)
    response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + htmlPage
    clientSocket.send(response)
    clientSocket.close()

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(('0.0.0.0', 80))
serverSocket.listen(1)


print()
print('Connection successful')
print(wlanStation.ifconfig())
begin_settime()
ledPin.on()
