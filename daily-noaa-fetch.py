#! /usr/bin/env python

import json
import requests
import datetime
import pytz
import astral
from astral.sun import sun
import os


today = datetime.datetime.today()
print("Tide data for:", today.ctime())

# NOAA Data
basic_info = "https://tidesandcurrents.noaa.gov/api/datagetter?date=today&product=predictions&datum=mllw&interval=hilo&format=json&units=metric&time_zone=lst_ldt&station="

adv_info = "https://tidesandcurrents.noaa.gov/api/datagetter?date=today&product=predictions&datum=mllw&format=json&units=metric&time_zone=lst_ldt&station="

stationID = "8418557"

# Get the data from NOAA
times = json.loads(requests.get(basic_info + stationID).text)['predictions']

# Calculate the time of dawn and dusk
# Note: only the timezone and lat+lon actually matter. The names are just for fun
ocean_park = astral.LocationInfo(
    name='Ocean Park',
    region='Maine',
    timezone='US/Eastern',
    latitude=43.5,
    longitude=-70.383)

sun_times = sun(ocean_park.observer, date=today, tzinfo=ocean_park.timezone)

timezone = pytz.timezone("US/Eastern")

# Schedule the execution of the other scripts
notify_times = []
for time in times:
    if (time['type'] == 'H'):
        continue

    # I love Python
    day, time = time['t'].split()
    year, month, day = [int(x) for x in day.split('-')]
    hour, minute = [int(x) for x in time.split(':')]

    # If we ask for predictions after the last low/high of the day, noaa will give us tomorrow's data
    if day > today.day:
        print("fetched tides for tomorrow, oops")
        continue
        
    notify_time = datetime.datetime(
        year,
        month,
        day,
        hour,
        minute,
        tzinfo=timezone)
        
    # Now, filter out the low tides that occur before dawn and after dusk
    if (sun_times['dawn'] < notify_time < sun_times['dusk']):
        print("low tide during sunlight!", notify_time)
    else:
        print("low tide during darkness.", notify_time)
        continue

    # Check to make sure that the low tide is in the future
    if notify_time < datetime.datetime.now(timezone):
        print("low tide in the past!")
        continue

    # We want to notify Dad BEFORE low tide, how long? 15 Min?    
    notify_times.append(notify_time - datetime.timedelta(minutes=15))

    
# If, for some reason there is no low tide during daylight hours, exit
if not notify_times:
    print("No low tides in the future today")
    exit()

# Use at to schedule the notification events for the right times today
for notify in notify_times:
    command = 'at ' + notify.time().isoformat('minutes') + ' -f /home/isaiah/OceanParkTideBot/low-tide-notify.sh 2>/dev/null'
    print(command)
    os.system(command)

# Use at to schedule the daily morning report to dad
morning_info = sun_times['dawn'] + datetime.timedelta(hours=1)

# Write the tide data to a file so other scripts can access the info
with open('logs/tides-today','w') as f:
    json.dump(times,f),

command = 'at ' + morning_info.time().isoformat('minutes') + ' -f /home/isaiah/OceanParkTideBot/morning-info.sh 2>/dev/null'
print(command)
os.system(command)
