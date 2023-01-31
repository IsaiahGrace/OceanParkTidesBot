#! /bin/sh

pushd /home/isaiah/OceanParkTideBot
python3 morning_info.py 1&>> logs/morning-info
popd
