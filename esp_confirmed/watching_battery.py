import network, urequests
from machine import Pin, ADC, Timer
from time import sleep
from math import floor

current_battery=54		#the accurate battery value from current run
temp_battery=54			#the last battery value
current_battery_level=5	#from 1 to 5
idel=0					#for battery accuracy
total=0					#the battery value from current run
count=0					#testing usage

#setting battery config
battery = ADC(Pin(34))
battery.atten(ADC.ATTN_11DB)       #Full range of 3.3v


HTTP_HEADERS = {'Content-Type': 'application/json'} 
THINGSPEAK_WRITE_API_KEY = '3PPYQEYKEMPHRW5B'

class watching_battery:
    def __init__(self):
        print('inited')
        
    def start(timer,self):
        sleep(2)
        global total
        global current_battery
        global temp_battery
        global idel
        global count
        global current_battery_level
        global led_trigger
        count+=1
       
        for x in range(20):
           total=total+battery.read()#取20次
        
        total = floor(total/20*1.8/100)#調至適合範圍
        #print(total)
        if(total==temp_battery):#穩定
            idel=idel+1
            if(idel==3):
                idel=0
                current_battery=temp_battery
        else:
            idel=0
            temp_battery=total
                
        if (current_battery >= 54):
            current_battery_level=5
        if (current_battery >= 50 and current_battery<54):
            current_battery_level=4
        if (current_battery >= 46 and current_battery<50):
            current_battery_level=3
        if (current_battery >= 41 and current_battery<46):
            current_battery_level=2
        if (current_battery >= 0 and current_battery<41):
            current_battery_level=1

        #thinkspeak for debug    
        '''current_battery_level_thinkspeak = {'field1':total,'field2':current_battery_level,'field3':current_battery,'field4':count} 
        request = urequests.post( 'http://api.thingspeak.com/update?api_key=' + THINGSPEAK_WRITE_API_KEY, json = current_battery_level_thinkspeak, headers = HTTP_HEADERS  )  
        request.close()'''
        
        total=0
    def collect_info_current_battery_level(self):
        global current_battery_level
        return current_battery_level
    def collect_info_current_battery(self):
        global current_battery
        return current_battery
    def collect_info_total(self):
        global total
        return total
    def collect_info_count(self):
        global count
        return count