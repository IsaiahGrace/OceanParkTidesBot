#! /bin/bash
set -e

if [[ $(pwd) != "/home/isaiah/OceanParkTidesBot" ]]; then
	echo "This script needs to be run from /home/isaiah/OceanParkTidesBot"
	echo "Do some hacking in here if you're not Isaiah."
	exit 1
fi

if [[ $(whoami) != "root" ]]; then
	echo "This script creates copies files to /etc/systemd/system/ and therefore needs to be run as root."
	exit 1
fi

echo "Copying service files to /etc/systemd/system."
cp -vf OPTB_daily_noaa_fetch.timer /etc/systemd/system/OPTB_daily_noaa_fetch.timer
cp -vf OPTB_daily_noaa_fetch.service /etc/systemd/system/OPTB_daily_noaa_fetch.service
cp -vf OPTB_morning_info.service /etc/systemd/system/OPTB_morning_info.service
cp -vf OPTB_low_tide_notify.service /etc/systemd/system/OPTB_low_tide_notify.service

echo "systemctl daemon-reload"
systemctl daemon-reload

echo "Enabling and Starting OPTB_daily_noaa_fetch.timer"
systemctl enable OPTB_daily_noaa_fetch.timer
systemctl start OPTB_daily_noaa_fetch.timer

echo "Status of OPTB_daily_noaa_fetch.timer"
systemctl status OPTB_daily_noaa_fetch.timer

echo "Status of OPTB_daily_noaa_fetch.service"
systemctl status OPTB_daily_noaa_fetch.service

echo "Installation complete."
