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

analog = ADC(0)
light1 = Pin(0, Pin.OUT)
soil1 = Pin(14, Pin.OUT)
led = Pin(2, Pin.OUT)
temp1 = dht.DHT11(Pin(5))
relay1 = Pin(4, Pin.OUT)
relay1.off()
led.off()

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


station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)
ap_if = network.WLAN(network.AP_IF)
ap_if.active(False)

while station.isconnected() == False:
  pass

def begin_settime():
  try:
    ntptime.host = "1.europe.pool.ntp.org"
    ntptime.settime()
  except Exception as e:
    html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>My MicroPython Web Server</title>
        </head>
        <body>
            <h1>BOOT</h1>
            <h2>"""+str(e)+"""</h2>
        </body>
        </html>
        """

    client_sock, client_addr = server_sock.accept()
    serve(client_sock,html)

def serve(client_sock,html):
    request = client_sock.recv(1024)
    response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + html
    client_sock.send(response)
    client_sock.close()

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.bind(('0.0.0.0', 80))
server_sock.listen(1)


print()
print('Connection successful')
print(station.ifconfig())
begin_settime()
led.on()
