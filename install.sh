#! /bin/bash
set -e

if [[ $(pwd) != "/home/isaiah/OceanParkTidesBot" ]]; then
	echo "This script needs to be run from /home/isaiah/OceanParkTidesBot"
	exho "Do some hacking in here if you're not Isaiah."
	exit 1
fi

if [[ $(whoami) != "root" ]]; then
	echo "This script creates symlinks to /etc/systemd/system/ and therefore needs to be run as root."
	exit 1
fi

echo "Creating symlinks in /etc/systemd/system for systemd services and timers."
ln -sf /etc/systemd/system/OPTB_daily_noaa_fetch.timer OPTB_daily_noaa_fetch.timer
ln -sf /etc/systemd/system/OPTB_daily_noaa_fetch.service OPTB_daily_noaa_fetch.service
ln -sf /etc/systemd/system/OPTB_morning_info.service OPTB_morning_info.service
ln -sf /etc/systemd/system/OPTB_low_tide_notify.service OPTB_low_tide_notify.service

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
