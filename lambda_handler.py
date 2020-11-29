import requests
import json
import telegram
import time

# NOAA Data
basic_info = "https://tidesandcurrents.noaa.gov/api/datagetter?date=today&product=predictions&datum=mllw&interval=hilo&format=json&units=metric&time_zone=lst_ldt&station="

adv_info = "https://tidesandcurrents.noaa.gov/api/datagetter?date=today&product=predictions&datum=mllw&format=json&units=metric&time_zone=lst_ldt&station="

stationID = "8418557"


# Telegram Data
token = "***REMOVED***"
chat_id = "***REMOVED***"


# Collect NOAA Tide data
times = json.loads(requests.get(basic_info + stationID).text)['predictions']

lows = [time for time in times if time['type'] == 'L']


# Telegram, send message
bot = telegram.Bot(token)
bot.sendMessage(chat_id, text=time.ctime() + '\n' + str(lows))
