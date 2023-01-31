#! /bin/sh

pushd /home/isaiah/OceanParkTideBot
python3 low_tide_notify.py 1&>> logs/low-tide-notify
popd
