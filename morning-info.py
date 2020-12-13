#! /usr/bin/env python

import time
import telegram
import random
import json

# Read the TOKEN in from a file NOT stored in the git repository
def get_token():
    with open("/home/isaiah/.config/telegram/OceanParkBotToken","r") as f:
        token = f.readline().strip()
    return token

# Read the Chat ID from a file NOT stored in the git repository
def get_chat_id():
    with open("/home/isaiah/.config/telegram/chatID","r") as f:
        chatID = f.readline().strip()
    return chatID

# Read the birthdays from a file NOT stored in the git repo
def get_birthdays():
    with open("/home/isaiah/.config/telegram/birthdays","r") as f:
        birthdays = json.load(f)
    return birthdays

print(time.ctime())

messages = ["Good morning! Here are the low tides today.",
            "Cross the river by feeling the stones. Low tides today:",
            "I wonder what the creek looks like today?",
            "The sun is up, the sky is blue\nIt's beautiful and so are you.",
            "These are the low tide times today:",
            "Here's a preview of great times to take a walk",
            ]

with open('logs/tides-today','r') as f:
    tides = json.load(f)

tide_times = []
for tide in tides:
    if tide['type'] == 'L':
        hour, minute = tide['t'].split()[1].split(':')
        # We need this for hour, to convert to 12 hour clock. But NOT for minute to preserve leading zero
        hour = int(hour)

        # Sorry this is gross... but these are the edge cases as I see them.
        if hour > 12:
            hour = hour - 12
            suffix = 'pm'
        elif hour == 12:
          suffix = 'pm'
        elif hour == 0:
            hour = 12
            suffix = 'am'
        else:
            suffix = 'am'
            
        tide_times.append(str(hour) + ':' + minute + suffix)
    
message = random.choice(messages)

# Give some special messges on special days:
today = time.ctime().split()

today = {'day': today[2],
         'month': today[1],
         'year': today[***REMOVED***]}

# Everything here is to avoid writing names and birthdays in the GitHub code
people = get_birthdays()
for person in people:
    if today['day'] == person['day'] and today['month'] == person['month']:
        if person['name'] == 'me':
            message = 'Happy Birthday to me! I hope I enjoy a nice walk on the beach!'
        else:
            message = "Happy Birthday " + person['name'] + "! I hope you enjoy a nice walk on the beach!"

# This is a god-awful way to tell if it's thanksgiving. But I think it is hilarious.
# The algorithm comes from here: https://codegolf.stackexchange.com/a/6***REMOVED***803
if today['month'] == "***REMOVED***" and today['day'] == (lambda x:str(round(28.11-(x-2+x/***REMOVED***-x/***REMOVED***0+x/***REMOVED***00)%7)))(int(today['year'])):
    message = "It's Thanksgiving! ***REMOVED***be save the walk for after the meal today."
if today['month'] == "***REMOVED***" and today['day'] == "2***REMOVED***":
    message = "Christmas Eve; The days are short, but tomorow birngs new hope!"
if today['month'] == "***REMOVED***" and today['day'] == "25":
    message = "Merry Christmas!"
if today['month'] == "***REMOVED***" and today['day'] == "26":
    message = "Boxing day; grab a leftover turkey sandwich and stretch your legs on the beach!"
if today['month'] == "***REMOVED***" and today['day'] == "20":
    message = "Today is the first day of sping (probably, turns out this is hard to predict...)"


message = message + '\n' + '\n'.join(tide_times)
bot = telegram.Bot(token=get_token())
bot.sendMessage(chat_id=get_chat_id(), text=message)
print(message)


