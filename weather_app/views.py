from django.shortcuts import render
from .utils import WeatherAPI

def index(request):
    """
    Handle Views for home page
    """
    if request.method == 'POST':
        city = request.POST['city']
        weather = WeatherAPI()
        weather_data = weather.get_weather(city)

        context = {
            'weather_data': weather_data,
        }

        return render(request, 'weather_app/current.html', context)
    return render(request, 'weather_app/current.html')

def forecast(request):
    """
    Handle Views for forecast page
    """
    if request.method == 'POST':
        city = request.POST['city']
        weather = WeatherAPI()
        location, forecast = weather.get_forecast(city)

        context = {
            'location': location,
            'forecast': forecast,
        }

        return render(request, 'weather_app/forecast.html', context)
    return render(request, 'weather_app/forecast.html')

def about(request):
    """
    Handle Views for about page
    """
    return render(request, 'weather_app/about.html')
