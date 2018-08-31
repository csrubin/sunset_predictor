#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 26 18:50:04 2018

@author: csrubin
"""

import pyowm
import socket
import geoip2.database
import sqlite3
from datetime import datetime

def main():
# Use socket module to get IP address
    hostname = socket.gethostname()
    IP = socket.gethostbyname(hostname)
    
    # Use geoip2 module to get zip code from IP address
    #    geo_db_path = '/Users/csrubin/Documents/Python/sunset_predictor/GeoLite2-City.mmdb'
    #    reader = geoip2.database.Reader(geo_db_path)
    #    response  = reader.city(IP)
    #    zipcode = response.postal.code
    
    # Instantiate object to communicate with Open Weather Map API
    API_KEY = '13ba58551921a308966ae0ff209caf68'
    owm = pyowm.OWM(API_KEY)
    
    # Create SQ: connection/cursor 
    db_path = '/Users/csrubin/Documents/Python/sunset_predictor/database.db'
    db = sqlite3.connect(db_path)
    c = db.cursor()
    
    # Instantiate weather object to query for data
    observation = owm.weather_at_zip_code('43201','US')
    w = observation.get_weather()
    
    # SQL commands to insert data into db 
    date = datetime.now()
    date = str(date)
    date = date[:10]
    day_data = (date,)
    c.execute('INSERT INTO days VALUES (NULL, ?)',day_data)
    data = get_data(w)
    c.execute('INSERT INTO weather_data VALUES (NULL, NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)' ,data)
    
    # Close db so that all changes are saved
    db.commit()
    db.close()


def get_data(obs_obj):
# Get data and manipulate it into correct types for db
    status = obs_obj.get_detailed_status()
    sunset_time = obs_obj.get_sunset_time('iso')
    clouds = obs_obj.get_clouds()
    rain = obs_obj.get_rain()
    rain = rain or 0
    snow = obs_obj.get_snow()
    snow = snow or 0
    wind = obs_obj.get_wind()
    wind_speed = wind['speed'] 
    wind_dir = wind['deg']
    visibility = obs_obj.get_visibility_distance()
    humidity =  obs_obj.get_humidity()
    pressure = obs_obj.get_pressure()
    pressure = pressure['press']
    temp = obs_obj.get_temperature('fahrenheit')
    temp = temp['temp']
    
    data = (status, sunset_time, clouds, rain, snow, wind_speed, wind_dir, visibility, humidity, pressure, temp)
    
    return data

if __name__=='__main__':
    main()
