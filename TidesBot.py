#!/usr/bin/env python

import telegram
import time

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

bot = telegram.Bot(token=get_token())
bot.sendMessage(chat_id=get_chat_id(), text=time.ctime())
    
