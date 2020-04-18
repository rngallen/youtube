from django.conf import settings
from django.db.models import Q
from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm
from django.contrib import messages

def home(request):
    city_weather = []
    key = settings.WEATHER_API_KEY
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            q = form.cleaned_data['name']
            search_url = f"https://api.openweathermap.org/data/2.5/weather?q={q}&appid={key}&units=metric"
            result = (requests.get(search_url)).json()
            if result['cod'] == 200:
                existing_city = City.objects.filter(city_id=result['id'])
                if existing_city:
                    messages.warning(
                        request, f"{result['name']} is already in the database!!!")
                else:
                    city = {
                        'city': result['name'],
                        'temperature': result['main']['temp'],
                        'description': (result['weather'][0]['description']).title(),
                        'icon': result['weather'][0]['icon'],
                        'city_id': result['id'],
                        'country': result['sys']['country'],
                    }
                    new_city = City(
                        city_id=city['city_id'], name=city['city'], country=city['country'])
                    new_city.save()
                    messages.success(
                        request, f"{result['name']} - {result['sys']['country']} added successfully")
            else:
                messages.warning(request, f"{q} in not a valid city fella!! ")
    all_city = City.objects.all()
    for q in all_city:
        search_url = f"https://api.openweathermap.org/data/2.5/weather?q={q}&appid={key}&units=metric"
        result = (requests.get(search_url)).json()
        '''city = {}'''
        city = {
            'city': result['name'],
            'temperature': result['main']['temp'],
            'description': (result['weather'][0]['description']).title(),
            'icon': result['weather'][0]['icon'],
            'city_id': result['id'],
            'country': result['sys']['country'],
        }
        city_weather.append(city)
    context = {
        'weather_data': city_weather,
        'form': CityForm()
    }
    return render(request, 'weather/index.html', context)
