#import the libraries

import random
import matplotlib.pyplot as plt
import matplotlib, numpy, sys
matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from matplotlib.figure import Figure

from matplotlib.ticker import FormatStrFormatter

import tkinter as Tk

import array

import random

import threading

import sched, time


#create the class to  generate random data

class Sensor:
    def __init__(self, min_temp: int = 0, max_temp: int = 40):
        self.min_value = min_temp
        self.max_value = max_temp 

    def __generator(self) -> float:
        m = self.max_value - self.min_value
        x = random.uniform(0, 1)
        c = self.min_value

        y = m * x + c
        return y

    @property
    def value(self):
        return self.__generator()


sensor = Sensor()

y_data = []
for i in range(30):
    y_data.append(sensor.value)# call the function to generate random values

#code to display the  random generated data to bar and line plots


s = sched.scheduler(time.time, time.sleep)

global counter

counter = 1

root = Tk.Tk()

root.title("Temprature Sensor Real Time Data")

f = Figure(figsize=(3,4), dpi=100)

ax = f.add_subplot(111)

canvas = FigureCanvasTkAgg(f, master=root)

x = []

y = []

def changeList():

    global y_data

    y_data.pop(0)  #Remove the first item in the list of values
    
    y_data.append(sensor.value)#Add a new random value to the end of the list

    show_bar(y_data[-1])

    root.after(500,changeList) #Sleep for a short while (0.5 of a second)

def show_bar(data):

    global ax

    global canvas

    global counter

    ax.clear()

    x.append(counter)

    y.append(data)

    counter = counter + 1

    canvas.draw()

    canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.NONE, expand=0.5)

    canvas.get_tk_widget().pack_forget()

    canvas.get_tk_widget().delete("all")

    f = Figure(figsize=(8,6), dpi=100)

    ax = f.add_subplot(111)

    ax.set_ylim(0, 40) 
    
    ax.yaxis.set_major_formatter(FormatStrFormatter('%d °C '))

    canvas = FigureCanvasTkAgg(f, master=root)
    
    ax.set_title("Sensor Temprature Vs Time ",color = "r")#set the grap title

    ax.bar(x[-30:],y[-30:], label="Bar plot", color='g')#draw the bar  plot

    ax.plot(x[-30:],y[-30:],label = "Line plot",color = "b")# draw the line plot

    ax.set_xlabel("Time(Second)")#set xlabel
    
    ax.set_ylabel("Temptrature Value(Celcius)")#set ylabel
    
    ax.legend()#put the legend
    
    ax.tick_params(axis = "x", which = "both", bottom = False, top = False, labelcolor='w')#only side ticks and labels

    canvas.draw()

    canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.NONE, expand=0.5)

#call the  method to displays the bar chart

for i in range(30):
    show_bar(y_data[i])

#Create a thread and set the target to the method in step 1

t = threading.Thread(target=changeList())

#set the  daemon property true

t.daemon = True

#start the thread

t.start()
# call the function to draws the rectangle and line
root.mainloop()
