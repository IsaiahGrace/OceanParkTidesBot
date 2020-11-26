import requests
import json

# The basic info just returns a list of times for high and low tide
basic_info = "https://tidesandcurrents.noaa.gov/api/datagetter?date=today&product=predictions&datum=mllw&interval=hilo&format=json&units=metric&time_zone=lst_ldt&station="

adv_info = "https://tidesandcurrents.noaa.gov/api/datagetter?date=today&product=predictions&datum=mllw&format=json&units=metric&time_zone=lst_ldt&station="

with open('stationID','r') as f:
    stationID = f.readline().strip()


times = json.loads(requests.get(basic_info + stationID).text)['predictions']

lows = [time for time in times if time['type'] == 'L']

for time in lows:
    print(time)
