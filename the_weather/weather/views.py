from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)

import requests
from .models import City
from .forms import CityForm, UserLoginForm, UserRegisterForm

def home(request):
   
    form = UserLoginForm(request.POST or None)

    context = {'form': form}

    return render(request, 'weather/home.html', context)




@login_required
def index(request):
    cities = City.objects.all() #return all the cities in the database

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=271d1234d3f497eed5b1d80a07b3fcd1'

    if request.method == 'POST': # only true if form is submitted
        try:
            form = CityForm(request.POST) # add actual request data to form for processing
            city_weather = requests.get(url.format(form)).json()
            form.save() # will validate and save if validate
        except:
            messages.error(request, "Enter correct city name!")
            return redirect('index')             

    form = CityForm()

    weather_data = []

    for city in cities:

        city_weather = requests.get(url.format(city)).json() #request the API data and convert the JSON to Python data types
        
        weather = {
            'city' : city,
            'temperature' : city_weather['main']['temp'],
            'description' : city_weather['weather'][0]['description'],
            'icon' : city_weather['weather'][0]['icon'],
            'country': city_weather['sys']['country'],
        }

        weather_data.append(weather) #add the data for the current city into our list
    
    context = {'weather_data' : weather_data, 'form' : form}

    return render(request, 'weather/index.html', context) #returns the index.html template






def login_view(request):
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect('index')

    context = {
        'form': form,
    }
    return render(request, "registration/login.html", context)


def register_view(request):
    next = request.GET.get('next')
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        if next:
            return redirect(next)
        return redirect('index')

    context = {
        'form': form,
    }
    return render(request, "registration/signup.html", context)


def logout_view(request):
    logout(request)
    return redirect('/')


def delete_city(request, city_name):
    City.objects.filter(name__iexact=city_name).delete()
    return redirect('index')
