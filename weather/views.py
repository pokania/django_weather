from django.shortcuts import render
from .models import City
from .forms import CityForm
import requests

url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid='

# Create your views here.

def index(request):
    form = CityForm()
    cities = City.objects.all()
    all_weather_data = []
    if request.method == "POST":
        form = CityForm(request.POST)
        form.save()
    for city in cities:
        weather_data = requests.get(url.format(city.name)).json()
        if weather_data['cod'] == 200:
            one_city_data = {
                'city_name' : city,
                'main' : weather_data['weather'][0]['main'],
                'description' : weather_data['weather'][0]['description'],
                'temp' : weather_data['main']['temp'],
                'icon' : weather_data['weather'][0]['icon']
            }
            all_weather_data.append(one_city_data)


    context = {
        'form' : form,
        'all_weather_data' : all_weather_data
    }
    return render(request, 'weather/index.html', context=context)
