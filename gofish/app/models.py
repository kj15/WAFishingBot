from __future__ import unicode_literals

import datetime
from django.db import models
from django.utils import timezone


class County(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True, default='')

    def __unicode__(self):
        return self.name


class Lake(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=1000)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    altitude =  models.FloatField(blank=True, null=True)
    size = models.FloatField(blank=True, null=True)
    rank = models.FloatField(blank=False, null=False, default=0.0)
    county = models.ForeignKey(County, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.name + ": " + str(self.rank)


class Fish(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class StockingData(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=1000)
    date = models.DateField(blank=True, null=True)
    amount = models.IntegerField(blank=True, null=True)
    fish = models.ForeignKey(Fish, on_delete=models.CASCADE)
    lake = models.ForeignKey(Lake, on_delete=models.CASCADE)

    def __unicode__(self):
        return str(self.date) + ": " + self.fish.name + " (" + str(self.amount) + ")"

class LakeStats(models.Model):
    id = models.AutoField(primary_key=True)
    last_updated = models.DateField(blank=True, null=True, default=datetime.date.today)
    min_size = models.FloatField(blank=True, null=True)
    avg_size = models.FloatField(blank=True, null=True)
    max_size = models.FloatField(blank=True, null=True)
    min_alt = models.FloatField(blank=True, null=True)
    avg_alt = models.FloatField(blank=True, null=True)
    max_alt = models.FloatField(blank=True, null=True)
