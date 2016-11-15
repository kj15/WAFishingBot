# -*- coding: utf-8 -*-
import os, sys, scrapy, re, datetime, json
import django

from lakes.items import LakeItem, StockingDataItem, FishItem, CountyItem
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
            lake_item = LakeItem()
            # if no links under this lake, cant get stocking data
            if len(lake.xpath(".//em")) != 0:
                lake_item['name'] = lake.xpath(".//strong/text()").extract()
                # lake_item['stocking_info'] = []
                data = lake.xpath(".//td[@valign='top']/text()").extract()
                lake_item['county'] = data[1]
                lake_item['altitude'] = re.sub(r'[^\d]', '', data[2])
                lake_item['size'] = re.sub(r'[^\d\.]', '', data[3])
                lat_long = lake.xpath(".//td[@rowspan='3']/text()")
                lake_item['latitude'] = re.sub(r'[^\d\.\-]', '', lat_long[0].extract())
                lake_item['longitude'] =  re.sub(r'[^\d\.\-]', '', lat_long[1].extract())
                lake_item['rank'] = 0.0
                yield lake_item
            else:
                link = lake.xpath(".//a[contains(@href,'/stocking/')]/@href").extract()
                if len(link) == 1:
                    req = Request("http://" + self.allowed_domains[0] + link[0], callback=self.parse_stocking)
                    req.meta['item'] = lake_item
                    yield req

    def parse_stocking(self, response):
        lake_item = response.meta['item']
        stocking_data = StockingDataItem()
        td_data = response.xpath("//table[@cellspacing='2']//td/text()").extract()
        p_data = response.xpath("//table[@cellspacing='2']//p/text()").extract()
        lake_item['name'] = td_data[0]
        lake_item['size'] = re.sub(r'[^\d\.]', '', td_data[-1])
        lake_item['altitude'] = re.sub(r'[^\d\.]', '', td_data[-2])
        lake_item['county'] = td_data[-3]
        lake_item['latitude'] = re.sub(r'[^\d\.\-]', '', p_data[1])
        lake_item['longitude'] = re.sub(r'[^\d\.\-]', '', p_data[2])

        #
        # # DO STOCKING FOR MULTIPLE FISH
        # stocking_data['date'] = td_data[1]
        # stocking_data['amount'] = td_data[2]
        # # stocked = []
        # # i = -1
        # # for fish in response.xpath("//table[@cellspacing='2']//strong"):
        # #     i+=2
        # #     while td_data[i] != u'\xa0' and td_data[i+1] != u'\xa0':
        # #         stock = StockingItem()
        # #         stock.fish = fish.xpath("./text()").extract()[0]
        # #         stock.date = datetime.datetime.strptime(str(td_data[i]), '%b %d, %Y')
        # #         stock.amt = td_data[i+1]
        # #         stocked.append(str(stock))
        # #         i+=2
        # # lake_item['stocking_info'] = stocked
        #
        # lake_item = self.rank(lake_item)
        yield lake_item

    def rank(self, lake_item):
        amt = float(str(lake_item['last_stocked_amt']).replace(',', ''))
        date_stocked = float(lake_item['last_stocked_date'].split(',')[1])
        size = float(lake_item['size'])
        alt = float(lake_item['alt'])
        current_year = float(datetime.date.today().year)
        cd = float(datetime.datetime.now().timetuple().tm_yday)

        # gavin has some weird math thing where the currentday value begins at sep1 (0) and ends at aug31 (365)
        # so 244 -> 0 and 243 -> 365
        if cd >= 244:
            current_day = cd - 244
        else:
            current_day = 365 - abs(cd - 243)


        stock_val = amt / (size * (current_year - date_stocked))*.2
        elev_val = 50000/(abs(alt - (.1513 * current_day)**2 + 49.5 * current_day + 5254))
        fish_rank = 2 * (elev_val)**1./2. + stock_val
        lake_item['rank'] = fish_rank
        return lake_item


