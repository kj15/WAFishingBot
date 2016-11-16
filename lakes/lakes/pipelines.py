# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import re
from items import LakeItem, StockingDataItem, FishItem, CountyItem
from app.models import Lake, StockingData, County, Fish

from scrapy.exceptions import DropItem


class NonePipeline(object):
    def __init__(self):
        self.nonallowable = ['url', 'date', 'title']

    def process_item(self, item, spider):
        for n in self.nonallowable:
            if (n not in item or item[n] is None) or (type(item) == 'list' and len(item) == 0):
                raise DropItem("Dropped item" + str(item) + ", had None value in nonallowable field: " + str(n))
        return item


class SavePipeline(object):
    def process_item(self, item, spider):
        return item.save()


class TypeFormattingPipeline(object):
    def __init__(self):
        # self.allowed_fields = ["stocking_info"]
        self.allowed_iter_fields = []
        self.float_fields = ['latitude', 'longitude', 'altitude', 'size']

    def process_item(self, item, spider):
        for k, v in item.iteritems():
            if k not in self.allowed_iter_fields and not isinstance(v, basestring) and self.is_iterable(v):
                if len(v) > 0:
                    item[k] = v[0]
                    if k in self.float_fields:
                        item[k] = float(v)
                else:
                    raise DropItem("Dropped " + str(item)  + " cause of blanks yo")
        return item

    def is_iterable(self, to_iter):
        try:
            iterator = iter(to_iter)
        except TypeError:
            return False
        else:
            return True
