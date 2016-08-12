# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy, datetime

class StockingItem(object):
        fish = ''
        date = datetime.date(1969,6,9)
        amt = 0

        def __str__(self):
                return self.fish + ": " + str(self.date) + "__" + self.amt

class LakesItem(scrapy.Item):
        name = scrapy.Field()
        alt = scrapy.Field()
        size = scrapy.Field()
        latitude = scrapy.Field()
        longitude = scrapy.Field()
        county = scrapy.Field()

        # stocking_info = scrapy.Field()
        last_stocked_date = scrapy.Field()
        last_stocked_amt = scrapy.Field()
        rank = scrapy.Field()
        
        
