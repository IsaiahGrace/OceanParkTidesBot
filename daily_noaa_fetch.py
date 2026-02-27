#! /usr/bin/env python
"""
Runs daily sometime before dawn, but after NOAA has updated their data for "today".
Downloads low tide times from NOAA and calculates daylight hours.
Uses systemd transient timers to schedule the morning briefing and the walk-time reminders.
"""

import astral
import astral.sun
import datetime
import json
import os
import requests
import zoneinfo


# Get the tide prediction data from NOAA.
basic_info = "https://tidesandcurrents.noaa.gov/api/datagetter?date=today&product=predictions&datum=mllw&interval=hilo&format=json&units=metric&time_zone=lst_ldt&station="
station_id = "8418557"
noaa_raw_data = requests.get(basic_info + station_id, timeout=60)
times = json.loads(noaa_raw_data.text)["predictions"]


# Calculate the time of dawn and dusk.
today = datetime.datetime.today()
timezone = zoneinfo.ZoneInfo("America/New_York")
ocean_park = astral.LocationInfo(timezone=timezone, latitude=43.5, longitude=-70.383)
sun_times = astral.sun.sun(ocean_park.observer, date=today, tzinfo=ocean_park.timezone)


# Calculate when to execute the low tide notifications.
notify_times = []
for time in times:
    # Ignore high tides
    if time["type"] != "L":
        continue

    # NOAA predictions are formatted like this: "2023-09-21 02:38".
    day, time = time["t"].split()
    year, month, day = [int(x) for x in day.split("-")]
    hour, minute = [int(x) for x in time.split(":")]

    # If we ask for predictions after the last low/high of the day, NOAA will give us tomorrow"s data.
    if day > today.day:
        print("Fetched tides for tomorrow, oops!")
        continue

    # Sometimes we get get yesterday's tide forecasts from NOAA.
    # Systemd will restart this service after 30mins if it exits with a non-zero exit code.
    # Hopefully by waiting a little bit we'll get today's predictions!
    if day < today.day:
        print("Fetched tides for yesterday, oops!")
        exit(1)

    low_tide_time = datetime.datetime(year, month, day, hour, minute, tzinfo=timezone)

    # Now, filter out the low tides that occur before dawn and after dusk.
    # Dad has requested an extra buffer after dusk, as he likes to walk in the evening.
    if sun_times["dawn"] < low_tide_time < sun_times["dusk"] + datetime.timedelta(hours=2):
        print("Low tide during sunlight.", low_tide_time)
    else:
        print("Low tide during darkness.", low_tide_time)
        continue

    # Check to make sure that the low tide is in the future.
    if low_tide_time < datetime.datetime.now(timezone):
        print("Low tide in the past!")
        continue

    # We want to notify Dad 60 minutes BEFORE low tide.
    notify_times.append(str(int((low_tide_time - datetime.timedelta(minutes=60)).timestamp())))


# Write the tide data to a file so other scripts can access the info.
with open("/tmp/tides_today.json", "w", encoding="utf-8") as f:
    json.dump(times, f)


# Schedule a morning message for one hour after dawn to preview low tide times for today.
morning_info_time = int((sun_times["dawn"] + datetime.timedelta(hours=1)).timestamp())
command = "systemd-run --on-calendar=@" + str(morning_info_time) + " --unit OPTB_morning_info.service"
print(command)
os.system(command)


# If there are any low tides worth notifying, schedule them as well.
if notify_times:
    command = "systemd-run --on-calendar=@" + ",@".join(notify_times) + " --unit OPTB_low_tide_notify.service"
    print(command)
    os.system(command)
else:
    print("No low tides in the future daylight hours today.")
