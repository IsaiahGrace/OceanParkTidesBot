#! /usr/bin/env python
"""
This script is scheduled to run by daily_noaa_fetch.py every morning one hour after dawn.
This publishes a message to the Telegram chat previewing the low tide times, as defined in the file logs/tides_today.json
"""

import time
import telegram
import random
import json
import asyncio
import fetch_secrets as secrets


messages = ["Good morning! Here are the low tides today.",
            "Cross the river by feeling the stones. Low tides today:",
            "I wonder what the creek looks like today?",
            "The sun is up, the sky is blue\nIt's beautiful and so are you.",
            "These are the low tide times today:",
            "Here's a preview of great times to take a walk",
            ]


# This is a confusing way to tell if it's thanksgiving. But it works!
# The algorithm comes from here: https://codegolf.stackexchange.com/a/64803
def thanksgiving_day(year_input):
    year = int(year_input)
    return str(round(28.11 - (year - 2 + year / 4 - year / 100 + year / 400) % 7))


def get_message():
    message = random.choice(messages)

    # Give some special messges on special days:
    ctime = time.ctime().split()

    today = {"day": ctime[2],
             "month": ctime[1],
             "year": ctime[4]}

    # Override the message if it's someones birthday!
    people = secrets.get_birthdays()
    for person in people:
        if today["day"] == person["day"] and today["month"] == person["month"]:
            message = "Happy Birthday " + person["name"] + "! I hope you enjoy a nice walk on the beach!"

    # Special message for Thanksgiving
    if today["month"] == "Nov" and today["day"] == thanksgiving_day(today["year"]):
        message = "It's Thanksgiving! Maybe save the walk for after the meal today."

    # Special message for Christmas eve, Christmas day, and Boxing day.
    if today["month"] == "Dec" and today["day"] == "24":
        message = "Christmas Eve; The days are short, but tomorow birngs new hope!"
    if today["month"] == "Dec" and today["day"] == "25":
        message = "Merry Christmas!"
    if today["month"] == "Dec" and today["day"] == "26":
        message = "Boxing day; grab a leftover turkey sandwich and stretch your legs on the beach!"

    # Special message for the first day of spring
    if today["month"] == "Mar" and today["day"] == "20":
        message = "Today is the first day of sping (probably, turns out this is hard to predict...)"

    return message


async def main():
    print(time.ctime())

    # Load today's tide times from the json file. The daily_noaa_fetch.py script updates this file daily at 3am.
    with open("logs/tides_today.json", "r", encoding="utf-8") as f:
        tides = json.load(f)

    tide_times = []
    for tide in tides:
        if tide["type"] != "L":
            continue

        hour, minute = tide["t"].split()[1].split(":")
        # We need this for hour, to convert to 12 hour clock. But NOT for minute to preserve leading zero
        hour = int(hour)

        # These are the edge cases as I see them.
        if hour > 12:
            hour = hour - 12
            suffix = "pm"
        elif hour == 12:
            suffix = "pm"
        elif hour == 0:
            hour = 12
            suffix = "am"
        else:
            suffix = "am"

        tide_times.append(str(hour) + ":" + minute + suffix)

    message = get_message()

    # Append the low tide times as new lines at the bottom of the message
    message = message + "\n" + "\n".join(tide_times)

    # Get the secrets from outside the git repo
    token = secrets.get_token()
    chat_id = secrets.get_chat_id()

    bot = telegram.Bot(token=token)
    await bot.sendMessage(chat_id=chat_id, text=message)

    print(message)


if __name__ == "__main__":
    asyncio.run(main())
