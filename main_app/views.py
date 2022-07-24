import imp
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Place, Photo
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
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


@login_required
def places_index(request):
    places = Place.objects.filter(user=request.user)
    return render(request, 'places/index.html', {'places': places})


@login_required
def places_detail(request, place_id):
    place = Place.objects.get(id=place_id)
    return render(request, 'places/detail.html', {'place': place})


@login_required
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


def signup(request):
    error_message = ''
    if request.method == 'POST':
        # This is how to create a 'user' form object
        # that includes the data from the browser
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # This will add the user to the database
            user = form.save()
            # This is how we log a user in via code
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid sign up - try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)


class PlaceCreate(LoginRequiredMixin, CreateView):
    model = Place
    fields = '__all__'
    success_url = '/places/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PlaceUpdate(LoginRequiredMixin, UpdateView):
    model = Place
    fields = ['cityName', 'fromDate', 'toDate', 'highlights']


class PlaceDelete(LoginRequiredMixin, DeleteView):
    model = Place
    success_url = '/places/'
