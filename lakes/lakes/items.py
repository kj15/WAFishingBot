# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class LakesItem(scrapy.Item):
        name = scrapy.Field()
        fish = scrapy.Field()
        altitutde = scrapy.Field()
        size = scrapy.Field()
        latitude = scrapy.Field()
        longitude = scrapy.Field()
        county = scrapy.Field()
        stocking_info = scrapy.Field()
        
        
