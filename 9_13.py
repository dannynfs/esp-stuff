import network, urequests
from machine import Pin, ADC
from time import sleep
from math import floor
HTTP_HEADERS = {'Content-Type': 'text/plain'} 
THINGSPEAK_WRITE_API_KEY = '3PPYQEYKEMPHRW5B' 
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

current_battery=53#the accurate battery value from current run
temp_battery=53#the last battery value
current_battery_level=5#from 1 to 5
idel=0#for battery accuracy
total=0#the battery value from current run
count=0#方便測試

print('connecting to network...')
wlan.connect('Danny the epic', '6666666668')
while not wlan.isconnected():
    pass
    
print('network config:', wlan.ifconfig())


battery = ADC(Pin(34))
battery.atten(ADC.ATTN_11DB)       #Full range of 3.3v

def watching_battery():
    sleep(1)
    global total
    global current_battery
    global temp_battery
    global idel
    global count
    for x in range(20):
       total=total+battery.read()#取20次
    
    total = floor(total/20*1.8/100)#調至適合範圍
    print(total)
    print(temp_battery)
    
    if(total==temp_battery):#穩定
        
        idel=idel+1
        if(idel==3):
            idel=0
            current_battery=temp_battery
    else:
        idel=0
        temp_battery=total
        print('in')
            
    if(current_battery>=52):
        current_battery_level=5
    elif(current_battery>=49):
        current_battery_level=4
    elif(current_battery>=45):
        current_battery_level=3
    elif(current_battery>=41):
        current_battery_level=2
    elif(current_battery>=0):
        current_battery_level=1
        
    request = urequests.post( 'destination' , data = current_battery_level, headers = HTTP_HEADERS )  
    request.close()
    total=0
 
while True:
  sleep(1)
  watching_battery()
  count=count+1
  
  


  



