import requests, json
from io import BytesIO
import csv
from datetime import datetime
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
import sys
import os


OPEN_WEATHER_TOKEN = '6f7a4550476814f8c5b3e7149e922aa2'
LOCATION = '53 Bridge St.'
LATITUDE = '40.702792'
LONGITUDE = '-73.984576'
UNITS = 'imperial'

BASE_URL = 'http://api.openweathermap.org/data/2.5/onecall?' 
URL = BASE_URL + 'lat=' + LATITUDE + '&lon=' + LONGITUDE + '&units=' + UNITS +'&appid=' + OPEN_WEATHER_TOKEN


response = requests.get(URL)
# Check status of code request
if response.status_code == 200:
    # get data in jason format
    data = response.json()

    # get current dict block
    current = data['current']
    # get current
    temp_current = current['temp']
    # get description
    weather = current['weather']
    descriptionreport = weather[0]['description']
    mainreport = weather[0]['main']
    print(descriptionreport)
    print(mainreport)
    # get icon url
    icon_code = weather[0]['icon']
    # icon_URL = 'http://openweathermap.org/img/wn/'+ icon_code +'@4x.png'
    
    # get daily dict block
    daily = data['daily']
    # get daily precip
    daily_precip_float = daily[0]['pop']
    #format daily precip
    daily_precip_percent = daily_precip_float * 100
    # get min and max temp
    daily_temp = daily[0]['temp']
    temp_max = daily_temp['max']
    temp_min = daily_temp['min']
            

    # Set strings to be printed to screen
    string_location = LOCATION
    string_temp_current = format(temp_current, '.0f') + u'\N{DEGREE SIGN}F'
    string_report = 'Now: ' + descriptionreport.title()
    string_temp_max = 'High: ' + format(temp_max, '>.0f') + u'\N{DEGREE SIGN}F'
    string_temp_min = 'Low:  ' + format(temp_min, '>.0f') + u'\N{DEGREE SIGN}F'
    string_precip_percent = 'Precip: ' + str(format(daily_precip_percent, '.0f'))  + '%'


    print('Location:', LOCATION)
    print('Temperature:', format(temp_current, '.0f'),u'\N{DEGREE SIGN}F') 
    print('Report:', descriptionreport.title())

    print('High:', format(temp_max, '.0f'), 'F')
    print('Low:', format(temp_min, '.0f'), 'F')
    print('Probabilty of Precipitation: ' + str(format(daily_precip_percent, '.0f'))  + '%')