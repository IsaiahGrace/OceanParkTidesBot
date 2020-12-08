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

print(time.ctime())

messages = ["Good morning! Here are the low tides today.\n",
            "Cross the river by feeling the stones. Low tides today:\n",
            "I wonder what the creek looks like today?\n",
            "The sun is up, the sky is blue\nIt's beautiful and so are you\n",
            ]

with open('logs/tides-today','r') as f:
    tides = json.load(f)

tide_times = []
for tide in tides:
    if tide['type'] == 'L':
        hour, minute = [int(x) for x in tide['t'].split()[1].split(':')]
        if hour > 12:
            hour = hour - 12
            suffix = 'pm'
        else:
            suffix = 'am'
            
        tide_times.append(str(hour) + ':' + str(minute) + suffix)
    
message = random.choice(messages) + '\n'.join(tide_times)

#bot = telegram.Bot(token=get_token())
#bot.sendMessage(chat_id=get_chat_id(), text=message)
print(message)

