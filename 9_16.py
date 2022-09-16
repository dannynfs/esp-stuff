import network, urequests
from machine import Pin, ADC, Timer
from time import sleep
from math import floor
HTTP_HEADERS = {'Content-Type': 'application/json'} 
THINGSPEAK_WRITE_API_KEY = '3PPYQEYKEMPHRW5B' 
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

current_battery=54#the accurate battery value from current run
temp_battery=54#the last battery value
current_battery_level=5#from 1 to 5
idel=0#for battery accuracy
total=0#the battery value from current run
count=0#方便測試
led_trigger=1
timer=Timer(-1)
led=Pin(15,Pin.OUT)

print('connecting to network...')
wlan.connect('Danny the epic', '6666666668')
while not wlan.isconnected():
    pass
    
print('network config:', wlan.ifconfig())


battery = ADC(Pin(34))
battery.atten(ADC.ATTN_11DB)       #Full range of 3.3v

def watching_battery(timer):
    
    sleep(2)
    global total
    global current_battery
    global temp_battery
    global idel
    global count
    global current_battery_level
    global led_trigger
    led.value(1)
    count+=1
   
    for x in range(20):
       total=total+battery.read()#取20次
    
    total = floor(total/20*1.8/100)#調至適合範圍
    print(total)
    #print(temp_battery)
    print(count)
    print(' ')
    
    if(total==temp_battery):#穩定
        
        idel=idel+1
        if(idel==3):
            idel=0
            current_battery=temp_battery
    else:
        idel=0
        temp_battery=total
        #print('in')
            
    if (current_battery >= 54):
        current_battery_level=5
    if (current_battery >= 49 and current_battery<54):
        current_battery_level=4
    if (current_battery >= 45 and current_battery<49):
        current_battery_level=3
    if (current_battery >= 41 and current_battery<45):
        current_battery_level=2
    if (current_battery >= 0 and current_battery<41):
        current_battery_level=1
    
    
        
    current_battery_level_thinkspeak = {'field1':total,'field2':current_battery_level,'field3':current_battery,'field4':count} 
    request = urequests.post( 'http://api.thingspeak.com/update?api_key=' + THINGSPEAK_WRITE_API_KEY, json = current_battery_level_thinkspeak, headers = HTTP_HEADERS  )  
    request.close()
    total=0
    
timer.init(period=10000,mode=Timer.PERIODIC,callback=watching_battery)
'''while True:
  sleep(1)
  watching_battery()
'''
  
  
  


  





