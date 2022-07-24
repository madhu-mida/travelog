from django.db import models
from datetime import date
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.


class Place(models.Model):
    cityName = models.CharField(max_length=100)
    fromDate = models.DateField('Visited On')
    toDate = models.DateField('Returned On')
    highlights = models.CharField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.cityName

    def get_absolute_url(self):
        return reverse('detail', kwargs={'place_id': self.id})


class Photo(models.Model):
    url = models.CharField(max_length=200)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for place_id: {self.place_id} @{self.url}"
