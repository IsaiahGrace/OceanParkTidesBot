#! /usr/bin/env python

import time
import telegram
import random

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

messages = ["The tide will be low in 15 minutes! Great time to go for a walk",
            "Low tide's in 15 mins!",
            "Take a break and go for a walk? Low tide is soon.",
            "It's time for a walk. The tide is low.",
            "The tide is *low* but I'm holdin' on\nI'm gonna be your number one",
            "Wade in the water\nWade in the water\nWade in the water, children\nGod is gonna trouble these waters",
            "Low tide in 15 minutes. Go check out the Guggenheim rocks!",
            "Perfect time for a walk! The tide is low right now!",
            ]

message = random.choice(messages)

#bot = telegram.Bot(token=get_token())
#bot.sendMessage(chat_id=get_chat_id(), text=message)
print(message)
