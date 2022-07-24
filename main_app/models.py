from django.db import models
from datetime import date
from django.urls import reverse

# Create your models here.


class Place(models.Model):
    cityName = models.CharField(max_length=100)
    fromDate = models.DateField('Visited On')
    toDate = models.DateField('Returned On')
    highlights = models.CharField(max_length=1000)

    def __str__(self):
        return self.cityName

    def get_absolute_url(self):
        return reverse('detail', kwargs={'place_id': self.id})
