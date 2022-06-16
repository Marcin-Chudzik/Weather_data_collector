import requests
import json

API_key = "7ad87a34dcc3c2be88b7ba506cf382d0"

# Warsaw geographical coordinates
warsaw_lat = 52.237049
warsaw_lon = 21.017532

# Gdansk geographical coordinates
gdansk_lat = 54.372158
gdansk_lon = 18.638306

# API call attributes
part = ['current']
measurement_units = "metric"
language = "pl"

warsaw_url = f"https://api.openweathermap.org/data/2.5/weather?lat=" \
             f"{warsaw_lat}&lon={warsaw_lon}&appid={API_key}&units{measurement_units}&lang{language}"

gdansk_url = f"https://api.openweathermap.org/data/2.5/weather?lat=" \
             f"{gdansk_lat}&lon={gdansk_lon}&appid={API_key}&units{measurement_units}&lang{language}"


def save_data(obj):
    with open('weather_data', 'a') as file:
        text: str = json.dumps(obj, sort_keys=True, indent=4)
        file.write(text)


warsaw_response = requests.get(warsaw_url)
save_data(warsaw_response.json())

gdansk_response = requests.get(gdansk_url)
save_data(gdansk_response.json())
