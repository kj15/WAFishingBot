# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem

class NoListsPipeline(object):
    def __init__(self):
        self.allowed_fields = ["stocking_info"]

    def process_item(self, item, spider):
        for k, v in item.iteritems():
            if k not in self.allowed_fields and not isinstance(v, basestring):
                if len(v) > 0:
                    item[k] = v[-1]
                else:
                    raise DropItem("Dropped " + str(item)  + " cause of blanks yo")
        return item
