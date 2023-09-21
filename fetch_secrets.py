"""
Fetches secrets not suitable to publish to GitHub.
* Telegram API token used to authenticate the bot
* Telegram chat ID used to identify the tides chat
* A JSON file listing family birthdays for special greetings
"""

import json

config_path = "/home/isaiah/.config/telegram/"


# Read the TOKEN in from a file NOT stored in the git repository
def get_token():
    with open(config_path + "OceanParkBotToken", "r", encoding="utf-8") as f:
        token = f.readline().strip()
    return token


# Read the Chat ID from a file NOT stored in the git repository
def get_chat_id():
    with open(config_path + "chatID", "r", encoding="utf-8") as f:
        chat_id = f.readline().strip()
    return chat_id


# Read the birthdays from a file NOT stored in the git repo
def get_birthdays():
    with open(config_path + "/birthdays", "r", encoding="utf-8") as f:
        birthdays = json.load(f)
    return birthdays
