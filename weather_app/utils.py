from datetime import datetime, timedelta
import requests
from django.conf import settings
import redis
import json


class WeatherAPI:
    def __init__(self):
        self.api_key = settings.WEATHER_API_KEY
        self.base_url = 'https://api.weatherapi.com/v1/{}?key={}&q={}'
        self.redis_client = redis.StrictRedis(host='localhost',
                                              port=6379, db=0)

    def get_weather(self, city: str) -> object:
        """ Fetch current weather data """
        cached_weather_data = self.redis_client.get(f'weather:{city}')
        if cached_weather_data:
            return json.loads(cached_weather_data.decode('utf-8'))

        weather_url = self.base_url.format('current.json', self.api_key, city)

        response = requests.get(weather_url).json()

        lt = response['location']['localtime']
        pfmt, ffmt = '%Y-%m-%d %H:%M', '%I:%M:%S %p'

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
            'local_time': datetime.strptime(lt, pfmt).strftime(ffmt),
        }

        name = f'weather:{city}'
        jdumps = json.dumps(weather_data).encode('utf-8')

        self.redis_client.setex(name, timedelta(minutes=10), jdumps)

        return weather_data

    def get_forecast(self, city: str) -> tuple:
        """ Fetch forecast weather data """
        cached_forecast_data = self.redis_client.get(f'forecast:{city}')
        if cached_forecast_data:
            return json.loads(cached_forecast_data.decode('utf-8'))

        forecast_url = self.base_url.format('forecast.json',
                                            self.api_key, city)
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
                'day': datetime.strptime(forecast['date'],
                                         '%Y-%m-%d').strftime('%a, %d %b %Y'),
                'max_temp': forecast['day']['maxtemp_c'],
                'min_temp': forecast['day']['mintemp_c'],
                'condition': forecast['day']['condition']['text'],
                'icon': forecast['day']['condition']['icon'],
                'humidity': forecast['day']['avghumidity'],
                'wind_speed': forecast['day']['maxwind_kph'],
            })
        data = [location, forecast_data]
        self.redis_client.setex(f'forecast:{city}', timedelta(minutes=30),
                                json.dumps(data).encode('utf-8'))

        return data
