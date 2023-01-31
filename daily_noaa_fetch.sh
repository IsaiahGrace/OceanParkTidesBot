#! /bin/sh

pushd /home/isaiah/OceanParkTideBot
python3 daily_noaa_fetch.py 1&>> logs/daily-noaa-fetch
popd
