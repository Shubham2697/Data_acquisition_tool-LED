import openpyxl                             #read, write excel Sheet
import time                                 #import time from system
from RPLCD import CharLCD                   #Configure LCD
import RPi.GPIO as GPIO                     #Configure GPIO pins
import Adafruit_ADS1x15                     #Import ADC to Rpi
import board                                #import different I2C boards from the library
import busio                                #configure BUS of Rpi
import adafruit_tsl2591			    #Import TSL (LUX sensor to the Rpi)

lcd = CharLCD(cols=16, rows=2, pin_rs=26, pin_e=19, pins_data=[13, 6, 5, 11],numbering_mode=GPIO.BCM)


#time
a11=0
acd=[]
m=0
h=0

def time_f(sec,minute,hour):
    sec+=4
    if(sec>59):
        minute=minute+1
        sec=0
        if(minute>59):
            hour=hour+1
            minute=0
    aaa=[sec,minute,hour]
    print(hour," ",minute," ",sec)
    return aaa

book=openpyxl.load_workbook('appending.xlsx')
sheet = book.active


#define lux sensor
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_tsl2591.TSL2591(i2c)



adc_value=[]
c=[]
adc = Adafruit_ADS1x15.ADS1115()
GAIN = 1



def teraadc():
    GAIN = 1
    a=[]
    temp = round((adc.read_adc(0,gain=GAIN)-adc.read_adc(3,gain=GAIN))*5.0/(32767*.0065),4)
    print(temp)
    lcd.write_string('Temp: '+str(temp))
    time.sleep(1);
    lcd.clear()
    
    volt = round(adc.read_adc(1,gain=GAIN)*4.6*72.2/32767,4)
    print(volt)
    lcd.write_string(u'Volt: '+str(volt))
    time.sleep(1);
    lcd.clear()
    
    curr = round(adc.read_adc(2,gain=GAIN)*4.6*0.95/32767,4)
    print(curr)
    lcd.write_string(u'Current: '+str(curr))
    time.sleep(1);
    lcd.clear()
    a=[temp,volt,curr]    
    return a

def luxsensor():
    lux = sensor.lux
    lcd.write_string(u'Lux: '+str(lux))
    time.sleep(1);
    lcd.clear()
    return lux

dim=sheet.dimensions
c=list(dim)
k=c[-1]
t=int(k)
while(True):
    #time
    acd=time_f(a11,m,h)
    a11=acd[0]
    m=acd[1]
    h=acd[2]
    
    adc_value=teraadc()

    adc_value.append(luxsensor())
    j=1
    for i in adc_value:
       
           sheet.cell(row=t+1,column=j).value=i
           j=j+1
           if(j>4):
               t=t+1
               break
    #time.sleep()
    book.save('appending.xlsx')



