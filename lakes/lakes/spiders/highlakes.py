# -*- coding: utf-8 -*-
import os, sys, scrapy, re

#import LakeItem, StockingItem
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
        counties = response.xpath("//div[@class='highlakesinfo']")
        print counties
        for lake in counties:
            # if no links under this lake, cant get stocking data
            if len(lake.xpath("//a").extract()) == 0:
                lake_item = LakeItem()
                lake_item['stocking_info'] = None
                lake_item['name'] = lake.xpath("//strong/text()").extract()[0]
                lake_item['fish'] = lake.xpath("//td[@colspan='3']/text()").extract()[0]
                lake_item['altitude'] = re.sub(r'[^\d]', '', lake.xpath("/table/tbody/tr[2]/td[1]").extract()[0])
                lake_item['size'] = re.sub(r'[^\d]', '', lake.xpath("/table/tbody/tr[2]/td[2]").extract()[0])
                lake_item['latitude'] = re.sub(r'[^\d\.]', '', lake.xpath("///table/tbody/tr[1]/td[2]/text()[1]").extract()[0])
                lake_item['longitude'] = re.sub(r'[^\d\.]', '', lake.xpath("///table/tbody/tr[1]/td[2]/text()[1]").extract()[0])
                lake_item['county'] = lake.xpath("/table/tbody/tr[2]/td[0]").extract()[0]
        pass
