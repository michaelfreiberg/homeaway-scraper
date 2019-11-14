# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import JSONRequest
from homeaway_scraper.items_pr import HomeawayScraperItem
from scrapy.exceptions import CloseSpider
import re
import json
import datetime
from calendar import monthrange

class HomeawaySpider(scrapy.Spider):
    name = 'homeaway_pr'

    allowed_domains = ['fewo-direkt.de']
    start_urls = ['https://www.fewo-direkt.de/']

    #def __init__(self, keywords='', *args,**kwargs):
    #    super(HomeawaySpider, self).__init__(*args, **kwargs)    

    def start_requests(self):
        f = open ('property-ids-all.txt', 'r')
        #f = open ('property-ids.txt', 'r')
        fl = f.readlines()

        for propertyId in fl:
            propertyId = propertyId.rstrip()
            url = ('https://www.fewo-direkt.de/ferienwohnung-ferienhaus/p{0}')  
            url = url.format(propertyId)
            yield scrapy.Request(url=url, callback=self.parse, meta={"propertyId" : propertyId})                    

    def parse(self, response):
        # Debugging response
        ## Write response to file
        #filename = 'ha_av-debug' + response.meta['propertyId'] + '.html'
        #with open(filename, 'wb') as f:
        #    f.write(response.body)
        #self.log('Saved file %s' % filename)

        listing = HomeawayScraperItem()
        
        listing['propertyId'] = response.meta['propertyId']

        listing['detailPageUrl'] = 'https://www.fewo-direkt.de/ferienwohnung-ferienhaus/p' + response.meta['propertyId']
        #listing['rateSections'] = json.loads(re.search(r'"rateSections":(.+),"unitRentalPolicy"',response.text).group(1))

        try:
            flatFees = json.loads(re.search(r'"flatFees":(\[[^\].]+\])',response.text).group(1))
        except:
            flatFees = {}
        
        try:
            rentNights = json.loads(re.search(r'"rentNights":(\[[^\].]+\])',response.text).group(1))
        except:
            rentNights = {}
        
        try:
            avgPrice = "{:5.2f}".format(sum(rentNights) / len(rentNights)).replace(".",",")
        except:
            avgPrice = 0

        listing['feeType'] = 'Average Price'
        listing['minAmount'] = avgPrice
        listing['maxAmount'] = avgPrice
        yield listing
        
        for f in flatFees:
            #  "type": "CLEANING_FEE",
            #     "appliesPer": "STAY",
            #     "description": "Reinigungsgeb\u00fchr",
            #     "minAmount": 7,
            #     "maxAmount": 7,
            #     "minAmountConverted": 7,
            #     "maxAmountConverted": 7

            try:
                listing['feeType'] = f.get('type')    
            except:
                listing['feeType'] = 'N/A'
            
            try:
                listing['minAmount'] = f.get('minAmount')
            except:
                listing['minAmount'] = 0
            
            try:
                listing['maxAmount'] = f.get('maxAmount')
            except:
                listing['minAmount'] = 0
            
            yield listing