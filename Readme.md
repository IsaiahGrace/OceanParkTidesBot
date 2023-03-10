# Ocean Park Tides Bot
This is a collection of simple Python scripts and Systemd timers/services which work together to send daily updates on the tides in Ocean Park Maine to a Telegram chat.

## Installation
To install, run the `install.sh` script with root privileges. The script copies service files to `/etc/systemd/system` so you can update the installation by re-running the install script.

## Dependencies
On Raspberry Pi OS (Debian Bullseye) these python packages are needed:

```
python3-python-telegram-bot
```

I've added **Astral v3.0** to the `astral` folder because Debian has a very outdated version of this package.
