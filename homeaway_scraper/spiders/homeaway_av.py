# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import JSONRequest
from homeaway_scraper.items_av import HomeawayScraperItem
from scrapy.exceptions import CloseSpider
import re
import json
import datetime
from calendar import monthrange

class HomeawaySpider(scrapy.Spider):
    name = 'homeaway_av'

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
        days_offset = 0        
        
        availability_calendar = json.loads(re.search(r'"availabilityCalendar":(.+\}\}\})',response.text).group(1))
        begin_date_str = availability_calendar.get('availability').get('dateRange').get('beginDate')
        begin_date = datetime.datetime.strptime(begin_date_str, '%Y-%m-%d')
        num_days_begin_date_month = (monthrange(begin_date.year, begin_date.month)[1])
        remaining_days_curr_month = num_days_begin_date_month - begin_date.day + 1
        
        availability_string = availability_calendar.get('availability').get('unitAvailabilityConfiguration').get('availability')
        available_days_curr_month = availability_string[:remaining_days_curr_month].count('Y')

        checkInAvailability_string = availability_calendar.get('availability').get('unitAvailabilityConfiguration').get('checkInAvailability')
        checkInAvailable_days_curr_month = checkInAvailability_string[:remaining_days_curr_month].count('Y')
        listing['propertyId'] = response.meta['propertyId']
        listing['detailPageUrl'] = 'https://www.fewo-direkt.de/ferienwohnung-ferienhaus/p' + response.meta['propertyId']
        listing['availabilityUpdated'] = availability_calendar.get('availability').get('availabilityUpdated')
        listing['month'] = begin_date.strftime('%B')
        listing['year'] = begin_date.year
        listing['available_days'] = available_days_curr_month
        listing['checkin_available_days'] = checkInAvailable_days_curr_month        
        #listing['month_availability_string'] = availability_string[:remaining_days_curr_month]
        #listing['days_offset'] = days_offset
        yield listing

        days_offset = days_offset + remaining_days_curr_month

        # current year
        for m in range(begin_date.month + 1, 13):
            month = datetime.date(begin_date.year, m, 1)
            num_days_month = monthrange(begin_date.year, m)[1]
            available_days_month = availability_string[days_offset:days_offset+num_days_month].count('Y')
            #month_availability_string = availability_string[days_offset:days_offset+num_days_month]
            checkInAvailable_days_month = checkInAvailability_string[days_offset:days_offset+num_days_month].count('Y')
            listing['propertyId'] = response.meta['propertyId']
            listing['detailPageUrl'] = 'https://www.fewo-direkt.de/ferienwohnung-ferienhaus/p' + response.meta['propertyId']
            listing['availabilityUpdated'] = availability_calendar.get('availability').get('availabilityUpdated')
            listing['month'] = month.strftime('%B')
            listing['year'] = begin_date.year
            listing['available_days'] = available_days_month
            listing['checkin_available_days'] = checkInAvailable_days_month
            
            #listing['month_availability_string'] = month_availability_string            
            #listing['days_offset'] = days_offset

            days_offset = days_offset + num_days_month
            yield listing            

        # next year
        for m in range(1, 13):
            month = datetime.date(begin_date.year + 1, m, 1)
            num_days_month = monthrange(begin_date.year + 1, m)[1]
            #month_availability_string = availability_string[days_offset:days_offset+num_days_month]
            available_days_month = availability_string[days_offset:days_offset+num_days_month].count('Y')
            checkInAvailable_days_month = checkInAvailability_string[days_offset:days_offset+num_days_month].count('Y')
            listing['propertyId'] = response.meta['propertyId']
            listing['detailPageUrl'] = 'https://www.fewo-direkt.de/ferienwohnung-ferienhaus/p' + response.meta['propertyId']
            listing['availabilityUpdated'] = availability_calendar.get('availability').get('availabilityUpdated')
            listing['month'] = month.strftime('%B')
            listing['year'] = begin_date.year + 1
            listing['available_days'] = available_days_month
            listing['checkin_available_days'] = checkInAvailable_days_month

            #listing['month_availability_string'] = month_availability_string            
            #listing['days_offset'] = days_offset

            days_offset = days_offset + num_days_month
            yield listing