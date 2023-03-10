#! /usr/bin/env python
"""
Runs daily sometime before dawn, but after NOAA has updated their data for "today".
Downloads low tide times from NOAA and calculates daylight hours.
Uses the unix "at" command to schedule a morning summary message for one hour after sunrise and messages for one hour before all low tide times that occur during daylight hours.
"""

from astral.sun import sun
import astral
import datetime
import json
import os
import pytz
import requests
import sys


today = datetime.datetime.today()

# NOAA Data
basic_info = "https://tidesandcurrents.noaa.gov/api/datagetter?date=today&product=predictions&datum=mllw&interval=hilo&format=json&units=metric&time_zone=lst_ldt&station="

adv_info = "https://tidesandcurrents.noaa.gov/api/datagetter?date=today&product=predictions&datum=mllw&format=json&units=metric&time_zone=lst_ldt&station="

station_id = "8418557"

# Get the data from NOAA
noaa_raw_data = requests.get(basic_info + station_id, timeout=60)
times = json.loads(noaa_raw_data.text)["predictions"]

# Calculate the time of dawn and dusk
# Note: Only the timezone and lat+lon actually matter. The names are just for fun.
ocean_park = astral.LocationInfo(
    name="Ocean Park",
    region="Maine",
    timezone="US/Eastern",
    latitude=43.5,
    longitude=-70.383)

sun_times = sun(ocean_park.observer, date=today, tzinfo=ocean_park.timezone)

timezone = pytz.timezone("US/Eastern")

# Schedule the execution of the other scripts
notify_times = []
for time in times:
    if time["type"] == "H":
        continue

    # I love Python
    day, time = time["t"].split()
    year, month, day = [int(x) for x in day.split("-")]
    hour, minute = [int(x) for x in time.split(":")]

    # If we ask for predictions after the last low/high of the day, noaa will give us tomorrow"s data
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
    if sun_times["dawn"] < notify_time < sun_times["dusk"]:
        print("low tide during sunlight!", notify_time)
    else:
        print("low tide during darkness.", notify_time)
        continue

    # Check to make sure that the low tide is in the future
    if notify_time < datetime.datetime.now(timezone):
        print("low tide in the past!")
        continue

    # We want to notify Dad 60 minutes BEFORE low tide
    notify_times.append(str(int((notify_time - datetime.timedelta(minutes=60)).timestamp())))


# Use at to schedule the daily morning report to dad
morning_info = sun_times["dawn"] + datetime.timedelta(hours=1)

# Write the tide data to a file so other scripts can access the info
with open("/tmp/tides_today.json", "w", encoding="utf-8") as f:
    json.dump(times, f)

# Schedule a morning message for one hour after dawn to preview low tide times for today
command = "systemd-run --on-calendar=@" + str(int(morning_info.timestamp())) + " --unit OPTB_morning_info.service"
print(command)
#os.system(command)

if notify_times:
    command = "systemd-run --on-calendar=@" + ',@'.join(notify_times) + " --unit OPTB_low_tide_notify.service"
    print(command)
    #os.system(command)
else:
    print("No low tides in the future daylight hours today")

