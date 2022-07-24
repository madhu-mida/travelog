import imp
from django.shortcuts import render
from django.http import HttpResponse
from .models import Place
from django.views.generic.edit import CreateView, UpdateView, DeleteView
# Create your views here.


# class Place:  # Note that parens are optional if not inheriting from another class
#     def __init__(self, cityName, fromDate, toDate, highlights):
#         self.cityName = cityName
#         self.fromDate = fromDate
#         self.toDate = toDate
#         self.highlights = highlights


# places = [
#     Place('Los Angeles', '07.22.2022', '15.22.2022',
#           'HollyWood, Santa Monica Pier'),
#     Place('Sachi', 'tortoise shell', 'diluted tortoise shell', 0),
#     Place('Raven', 'black tripod', '3 legged cat', 4)
# ]


def home(request):
    return HttpResponse('<h1>Hello /ᐠ｡‸｡ᐟ\ﾉ</h1>')


def about(request):
    return render(request, 'about.html')


def places_index(request):
    places = Place.objects.all()
    return render(request, 'places/index.html', {'places': places})


def places_detail(request, place_id):
    place = Place.objects.get(id=place_id)
    return render(request, 'places/detail.html', {'place': place})


class PlaceCreate(CreateView):
    model = Place
    fields = '__all__'
    success_url = '/places/'


class PlaceUpdate(UpdateView):
    model = Place
    fields = ['cityName', 'fromDate', 'toDate', 'highlights']


class PlaceDelete(DeleteView):
    model = Place
    success_url = '/places/'
