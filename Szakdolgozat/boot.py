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

insertUrl = ""
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
  except:
    begin_settime()


print()
print('Connection successful')
begin_settime()
led.on()
