import openpyxl                             #read, write excel Sheet
import time                                 #import time from system
from RPLCD import CharLCD                   #Configure LCD
import RPi.GPIO as GPIO                     #Configure GPIO pins
import Adafruit_ADS1x15                     #Import ADC to Rpi
import board
import busio
import adafruit_tsl2591
import threading
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import queue

temperature=queue.Queue(10)
voltage=queue.Queue(10)
current=queue.Queue(10)
luxxx=queue.Queue(10)
fig=plt.figure(1)
global w
global x
global y
global z
w=[]
x=[]
y=[]
z=[]
lcd = CharLCD(cols=16, rows=2, pin_rs=26, pin_e=19, pins_data=[13, 6, 5, 11],numbering_mode=GPIO.BCM)
lcd.clear()

class final(threading.Thread):
    def run(self):        
        #time
        a11=0
        acd=[]
        m=0
        h=0

        def time_f(sec,minute,hour):
            
            sec+=1
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
            global w
            global x
            global y
            GAIN = 1
            a=[]
            
            temp = round((adc.read_adc(0,gain=GAIN)-adc.read_adc(3,gain=GAIN))*5.0/(32767*.0065),4)
            print("Temp",temp)
            lcd.write_string('Temp: '+str(temp))
            temperature.put(temp)
            w=list(temperature.queue)
            if (temperature.full()):
                temperature.get()
            time.sleep(1)
            lcd.clear()
            
            volt = round(adc.read_adc(1,gain=GAIN)*4.8*72.2/32767,4)
            print("Voltage",volt)
            lcd.write_string(u'Volt: '+str(volt))
            voltage.put(volt)
            x=list(voltage.queue)
            if (voltage.full()):
                voltage.get()
            time.sleep(1)
            lcd.clear()
            
            curr = round(adc.read_adc(2,gain=GAIN)*4.6*0.95/32767,4)
            print("Current",curr)
            lcd.write_string(u'Current: '+str(curr))
            current.put(curr)
            y=list(current.queue)
            if (current.full()):
                current.get()
            time.sleep(1)
            lcd.clear()
            
            a=[temp,volt,curr]    
            return a
        
        def luxsensor():
            global z
            lux = round(sensor.lux*2, 4)
            print("Lux", lux)
            lcd.write_string(u'Lux: '+str(lux))
            luxxx.put(lux)
            if (luxxx.full()):
                luxxx.get()
            z=list(luxxx.queue)
            time.sleep(1)
            lcd.clear()
            return lux

        dim=sheet.dimensions
        c=list(dim)
        k=c[-1]
        t=int(k)

        while(True):
            print("\n")
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
            book.save('appending.xlsx')
            

class demo(threading.Thread):
    def animate(i):
        time.sleep(1)
        global w
        global x
        global y
        global z
        tem=w[-10:]
        volt=x[-10:]
        curr=y[-10:]
        luxx=z[-10:]
        ax1=fig.add_subplot(221)
        ax1.clear()
        ax1.grid()
        ax1.plot(tem)
        plt.ylabel("Temperature in degreeC")
        plt.xlabel("N")
        ax2=fig.add_subplot(222)
        ax2.clear()
        ax2.grid()
        ax2.plot(volt)
        plt.ylabel("Voltage in volt")
        plt.xlabel("N")
        ax3=fig.add_subplot(223)
        ax3.clear()
        ax3.grid()
        ax3.plot(curr)
        plt.ylabel("current in amp")
        plt.xlabel("N")
        ax4=fig.add_subplot(224)
        ax4.clear()
        ax4.grid()
        ax4.plot(luxx)
        plt.ylabel("Intensity In lux")
        plt.xlabel("N")
    while(1):
        ani=animation.FuncAnimation(fig, animate, interval=500)
        plt.show()


t1=final()
t2=demo()

t2.start()
time.sleep(0.2)
t1.start()
