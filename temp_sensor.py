import os
import glob
import pyowm
from time import sleep
import plotly.plotly as py
from plotly.graph_objs import *
#API KEYS
#PLOTLY
py.sign_in('USERNAME', 'API KEY')
#PYOWM
key = ('API KEY')

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

#VARIABLES
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
global temp_c
x = ['10:00','11:00','12:00','13:00','14:00']
y = []
sensor = []

def get_weather(n):
    owm = pyowm.OWM(key)
    observation = owm.weather_at_place((n))
    w = observation.get_weather()
    a = (w.get_temperature('celsius'))
    print("The current temperature at",(n),"is",a['temp'])
    y.append(a['temp'])

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    global temp_c
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()

    equals_pos = lines[1].find('t=')

    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c


for i in range(5):
    get_weather('Blackpool,uk')
    read_temp()
    sensor.append(temp_c)
    print(temp_c)
    sleep(5)

trace0 = Scatter(x=(x),y=(y))
trace1 = Scatter(x=(x),y=(sensor))

data = Data([trace0, trace1])

unique_url = py.plot(data, filename = 'Blackpool Temperature')
