# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy, datetime
from scrapy_djangoitem import DjangoItem

from app.models import Lake, StockingData, County, Fish

class StockingDataItem(DjangoItem):
        django_model = StockingData

class FishItem(DjangoItem):
        django_model = Fish

class CountyItem(DjangoItem):
        name=  scrapy.Field()

class LakeItem(DjangoItem):
        django_model = Lake


        
        
