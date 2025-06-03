import requests
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("API_KEY")
weather_base_url = "https://api.openweathermap.org/data/2.5/weather"
icon_url = "http://openweathermap.org/img/wn/{}@4x.png"
mistake_message = "Oops! Something went wrong. Please try again."

class Weather:
    def __init__(self):
        self.icon = None
        self.city = None
        self.country = None
        self.temperature = None
        self.description = None

    def get_weather_data(self, city):
        weather_url = f"{weather_base_url}?q={city}&appid={api_key}"
        response = requests.get(weather_url)
        if response.status_code == 200:
            weather_data = response.json()
            if str(weather_data.get("cod")) == "200":
                try:
                    self.icon = weather_data['weather'][0]['icon']
                    self.city = weather_data['name']
                    self.country = weather_data['sys']['country']
                    self.temperature = f"{int(weather_data['main']['temp'] - 273.15)} °C"
                    self.description = weather_data['weather'][0]['description']
                    return True
                except (KeyError, IndexError, TypeError):
                    return mistake_message
        return mistake_message