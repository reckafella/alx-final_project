from datetime import datetime
import requests
from django.conf import settings


class WeatherAPI:
    def __init__(self):
        self.api_key = settings.WEATHER_API_KEY
        self.base_url = 'https://api.weatherapi.com/v1/{}?key={}&q={}'

    def get_weather(self, city: str) -> object:
        """ Fetch current weather data """
        weather_url = self.base_url.format('current.json', self.api_key, city)

        response = requests.get(weather_url).json()
        weather_data = {
            'city': response['location']['name'],
            'country': response['location']['country'],
            'temp_c': response['current']['temp_c'],
            'lat': response['location']['lat'],
            'lon': response['location']['lon'],
            'humidity': response['current']['humidity'],
            'wind_speed': response['current']['wind_kph'],
            'condition': response['current']['condition']['text'],
            'icon': response['current']['condition']['icon'],
            'local_time': datetime.strptime(response['location']['localtime'], '%Y-%m-%d %H:%M'),
        }

        return weather_data

    def get_forecast(self, city: str) -> tuple:
        """ Fetch forecast weather data """
        forecast_url = self.base_url.format('forecast.json', self.api_key, city)
        forecast_url += '&days=7'

        response = requests.get(forecast_url).json()

        forecast_data = []
        location = {
            'city': response['location']['name'],
            'country': response['location']['country'],
            'lat': response['location']['lat'],
            'lon': response['location']['lon'],
        }

        for forecast in response['forecast']['forecastday']:
            forecast_data.append({
                'day': forecast['date'],
                'date': datetime.strptime(forecast['date'], '%Y-%m-%d').strftime('%a'),
                'max_temp': forecast['day']['maxtemp_c'],
                'min_temp': forecast['day']['mintemp_c'],
                'condition': forecast['day']['condition']['text'],
                'icon': forecast['day']['condition']['icon'],
                'humidity': forecast['day']['avghumidity'],
                'wind_speed': forecast['day']['maxwind_kph'],
            })

        return location, forecast_data
