# -*- coding: utf-8 -*-
import os, sys, scrapy, re, datetime, json

from lakes.items import LakesItem, StockingItem
from scrapy.contrib.spiders import CrawlSpider, Rule, Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

class HighlakesSpider(scrapy.Spider):
    name = "highlakes"
    allowed_domains = ["wdfw.wa.gov"]
    start_urls = (
        'http://wdfw.wa.gov/fishing/washington/highlakes/GeoLocation/56/',
        'http://wdfw.wa.gov/fishing/washington/highlakes/GeoLocation/573/',
        'http://wdfw.wa.gov/fishing/washington/highlakes/GeoLocation/569/',
        'http://wdfw.wa.gov/fishing/washington/highlakes/GeoLocation/42/',
        'http://wdfw.wa.gov/fishing/washington/highlakes/GeoLocation/567/',
        'http://wdfw.wa.gov/fishing/washington/highlakes/GeoLocation/600/',
        'http://wdfw.wa.gov/fishing/washington/highlakes/GeoLocation/52/',
    )
    
    # rules = (
    #     Rule(SgmlLinkExtractor(allow=(), restrict_xpaths=("//td[@colspan='4']/a")), callback='parse_page', follow=True)
    # )

    def parse(self, response):
        for lake in response.xpath("//div[@class='highlakesinfo']/div"):
            lake_item = LakesItem()
            # if no links under this lake, cant get stocking data
            if len(lake.xpath(".//em")) != 0:
                lake_item['name'] = lake.xpath(".//strong/text()").extract()
                # lake_item['stocking_info'] = []
                data = lake.xpath(".//td[@valign='top']/text()").extract()
                lake_item['county'] = data[1]
                lake_item['alt'] = re.sub(r'[^\d]', '', data[2])
                lake_item['size'] = re.sub(r'[^\d\.]', '', data[3])
                lat_long = lake.xpath(".//td[@rowspan='3']/text()")
                lake_item['latitude'] = re.sub(r'[^\d\.\-]', '', lat_long[0].extract())
                lake_item['longitude'] =  re.sub(r'[^\d\.\-]', '', lat_long[1].extract())
                yield lake_item
            else:
                link = lake.xpath(".//a[contains(@href,'/stocking/')]/@href").extract()
                if len(link) == 1:
                    req = Request("http://" + self.allowed_domains[0] + link[0], callback=self.parse_stocking)
                    req.meta['item'] = lake_item
                    yield req

    def parse_stocking(self, response):
        lake_item = response.meta['item']
        td_data = response.xpath("//table[@cellspacing='2']//td/text()").extract()
        p_data = response.xpath("//table[@cellspacing='2']//p/text()").extract()
        lake_item['name'] = td_data[0]
        lake_item['size'] = re.sub(r'[^\d\.]', '', td_data[-1])
        lake_item['alt'] = re.sub(r'[^\d\.]', '', td_data[-2])
        lake_item['county'] = td_data[-3]
        lake_item['latitude'] = re.sub(r'[^\d\.\-]', '', p_data[1])
        lake_item['longitude'] = re.sub(r'[^\d\.\-]', '', p_data[2])


        lake_item['last_stocked_date'] = td_data[1]
        lake_item['last_stocked_amt'] = td_data[2]
        # stocked = []
        # i = -1
        # for fish in response.xpath("//table[@cellspacing='2']//strong"):
        #     i+=2
        #     while td_data[i] != u'\xa0' and td_data[i+1] != u'\xa0':
        #         stock = StockingItem()
        #         stock.fish = fish.xpath("./text()").extract()[0]
        #         stock.date = datetime.datetime.strptime(str(td_data[i]), '%b %d, %Y')
        #         stock.amt = td_data[i+1]
        #         stocked.append(str(stock))
        #         i+=2
        # lake_item['stocking_info'] = stocked
        yield lake_item

    def is_digit(self, test):
        return re.match(r'\d', test)
