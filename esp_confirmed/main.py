import ubinascii
import ujson
import network, urequests
import machine
import json
from machine import Pin, ADC, Timer
from time import sleep
from math import floor
import esp32ble

# environment vars (初次使用或更換環境時，請務必確認)
model = 2   # model 1: controlled by itself; model 2: controlled by management system
server_url = 'http://192.168.19.4:5000'  # has to set if it's model 2
wifi_id = 'Danny the epic'  # has to set if it's model 2
wifi_pwd = '6666666668'  # has to set if it's model 2

# get device unique ID
unique_id = ubinascii.hexlify(machine.unique_id()).decode()  # bytes(2) -> bytes(16) -> string
print('device unique ID: ' + unique_id)

# BLE init & start broadcasting
ble = esp32ble.ESP32_BLE('2', unique_id)

#global function
timer = Timer(-1)  # for timer function
timer_get = Timer(-1)
current_battery = 54  # the accurate battery value from current run
temp_battery = 54  # the last battery value
current_battery_level = 5  # from 1 to 5
idel = 0  # for battery accuracy
total = 0  # the battery value from current run
count = 0
battery = ADC(Pin(34))
battery.atten(ADC.ATTN_11DB)  # full range of 3.3v

# function: setting battery config
def watching_battery(timer):
    sleep(2)
    global total
    global current_battery
    global temp_battery
    global idel
    global count
    global current_battery_level
    count += 1
    print(count)
   
    for x in range(20):
       total = total + battery.read()  # 取20次
    
    total = floor(total / 20 * 1.8 / 100)  # 調至適合範圍
    if (total == temp_battery):  # 穩定
        idel = idel + 1
        if (idel == 3):
            idel = 0
            current_battery = temp_battery
    else:
        idel = 0
        temp_battery = total
            
    if (current_battery >= 54):
        current_battery_level = 5
    if (current_battery >= 50 and current_battery < 54):
        current_battery_level = 4
    if (current_battery >= 46 and current_battery < 50):
        current_battery_level = 3
    if (current_battery >= 41 and current_battery < 46):
        current_battery_level = 2
    if (current_battery >= 0 and current_battery < 41):
        current_battery_level = 1
        
    current_battery_level_json = ujson.dumps({'UUID': unique_id, 'Battery': current_battery_level})
    battery_send = urequests.post(server_url + '/renewBattery', data=current_battery_level_json)  # remember to confirm IP address
    battery_send.close()
    

def get_commend(timer_get):
    global ble
    #server_url+'/table/BLE/'+unique_id
    order=urequests.get(url=server_url+'/table/BLE/'+unique_id).text
    print(order)
    order_json=ujson.loads(order)
    print(order_json['Status'])
    
    if(order_json['Status']==0):
        ble.state("false")
        print("close")
        
    else:
        ble = esp32ble.ESP32_BLE('2', unique_id)
        print("open")


if (ble.is_ble_connected):
    ble.send()

# run if it's model 2
if (model == 2):
    # Wi-Fi connecting
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    print('connecting to network...')
    wlan.connect(wifi_id, wifi_pwd)
    while not wlan.isconnected():
        pass
    print('network config:', wlan.ifconfig())

    # enroll new device
    post_data_json = ujson.dumps({'UUID': unique_id, 'tx': ble.tx_uuid, 'rx': ble.rx_uuid, 'nus': ble.service_uuid})  # obj -> JSON string
    #res = urequests.post(server_url + '/newDevice', data=post_data_json)
    #res.close()
   # timer.init(period=120000, mode=Timer.PERIODIC, callback=watching_battery)
    timer_get.init(period=10000, mode=Timer.PERIODIC, callback=get_commend)




