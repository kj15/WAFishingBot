# -*- coding: utf-8 -*-
import os, sys, scrapy, re

from lakes.items import LakesItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

class HighlakesSpider(scrapy.Spider):
    name = "highlakes"
    allowed_domains = ["wdfw.wa.gov/"]
    start_urls = (
        'http://wdfw.wa.gov/fishing/washington/highlakes/GeoLocation/56/',
        'http://wdfw.wa.gov/fishing/washington/highlakes/GeoLocation/573/',
        'http://wdfw.wa.gov/fishing/washington/highlakes/GeoLocation/569/',
        'http://wdfw.wa.gov/fishing/washington/highlakes/GeoLocation/42/',
        'http://wdfw.wa.gov/fishing/washington/highlakes/GeoLocation/567/',
        'http://wdfw.wa.gov/fishing/washington/highlakes/GeoLocation/600/',
        'http://wdfw.wa.gov/fishing/washington/highlakes/GeoLocation/52/' 
    )
    
    # rules = (
    #     Rule(SgmlLinkExtractor(allow=(), restrict_xpaths=("//td[@colspan='4']/a")), callback='parse_page', follow=True)
    # )

    def parse(self, response):
        for lake in response.xpath("//div[@class='highlakesinfo']/div"):
            # if no links under this lake, cant get stocking data
            if len(lake.xpath(".//em")) != 0:
                lake_item = LakesItem()
                lake_item['name'] = lake.xpath(".//strong/text()").extract()
                lake_item['stocking_info'] = None
                data = lake.xpath(".//td[@valign='top']/text()").extract()
                lake_item['county'] = data[1]
                lake_item['alt'] = re.sub(r'[^\d]', '', data[2])
                lake_item['size'] = re.sub(r'[^\d\.]', '', data[3])
                lake_item['fish'] = data[4]
                lat_long = lake.xpath(".//td[@rowspan='3']/text()")
                lake_item['latitude'] = re.sub(r'[^\d\.]', '', lat_long[0].extract())
                lake_item['longitude'] =  re.sub(r'[^\d\.]', '', lat_long[1].extract())
                yield lake_item
        pass


    def is_digit(self, test):
        return re.match(r'\d', test)
