import imp
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Place, Photo
from django.views.generic.edit import CreateView, UpdateView, DeleteView
import uuid
import boto3
S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'travelog-ms-95'
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


def add_photo(request, place_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + \
            photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            # we can assign to cat_id or cat (if you have a cat object)
            photo = Photo(url=url, place_id=place_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', place_id=place_id)


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
