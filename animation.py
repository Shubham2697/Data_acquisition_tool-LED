import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

fig=plt.figure(1)

def animate(i):
    time.sleep(0.1)
    af=pd.read_excel("appending.xlsx")
    df=af.tail(10)
    tem=df["temp"]
    volt=df["voltage"]
    curr=df["current"]
    luxx=df["lux"]
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

