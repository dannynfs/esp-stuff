import ubinascii
import ujson
import network, urequests
import machine
from machine import Pin, ADC, Timer
import watching_battery,esp32ble
HTTP_HEADERS = {'Content-Type': 'application/json'} 
THINGSPEAK_WRITE_API_KEY = '3PPYQEYKEMPHRW5B'
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

#global vars
timer=Timer(-1)			#for timer function

# get device unique ID
unique_id = ubinascii.hexlify(machine.unique_id()).decode()  # bytes(2) -> bytes(16) -> string
print('device unique ID: ' + unique_id)

#wifi connecting
print('connecting to network...')
wlan.connect('Hello Stranger', '00000000')
while not wlan.isconnected():
    pass
    
print('network config:', wlan.ifconfig())


battery_superviser=watching_battery.watching_battery()
battery_superviser.__init__()
ble = esp32ble.ESP32_BLE('2', unique_id)  # model 1: controlled by itself; model 2: controlled by management system
#timer.init(period=1000,mode=Timer.PERIODIC,callback=battery_superviser.start(timer))

while True:
    
    if ble.is_ble_connected:
        ble.send()
    # POST device unique ID and battery info to server
    battery_superviser.start(timer)
    current_battery_level=battery_superviser.collect_info_current_battery_level()
    current_battery=battery_superviser.collect_info_current_battery()
    total=battery_superviser.collect_info_total()
    count=battery_superviser.collect_info_count()
    print(count)
    
    if(count==1):
        post_data_json = ujson.dumps({'UUID': unique_id})  # obj -> JSON string
        #current_battery_level_thinkspeak = {'field1':total,'field2':current_battery_level,'field3':current_battery,'field4':count} 
        #request = urequests.post( 'http://api.thingspeak.com/update?api_key=' + THINGSPEAK_WRITE_API_KEY, json = current_battery_level_thinkspeak, headers = HTTP_HEADERS  )  
        res = urequests.post('http://192.168.0.103:5000/newDevice', data=post_data_json)  # remember to confirm IP address
        res.close()
        
    current_battery_level_json= ujson.dumps({'current_battery_level': current_battery_level})
    battery_send = urequests.post('http://192.168.0.103:5000/bettery_level', data=current_battery_level_json)  # remember to confirm IP address
        
    
  
  


  






