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

    def __init__(self, keywords='', *args,**kwargs):
        super(HomeawaySpider, self).__init__(*args, **kwargs)    

    def start_requests(self):
        url = ('https://www.fewo-direkt.de/ferienwohnung-ferienhaus/p1593409vb')  
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        # Debugging response
        ## Write response to file
        filename = 'ha_av-debug.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

        listing = HomeawayScraperItem()
        availability = {}        
        checkInAvailability = {}
        days_offset = 0

        
        availability_calendar = json.loads(re.search(r'"availabilityCalendar":(.+\}\}\})',response.text).group(1))
        begin_date_str = availability_calendar.get('availability').get('dateRange').get('beginDate')
        begin_date = datetime.datetime.strptime(begin_date_str, '%Y-%m-%d')
        num_days_begin_date_month = (monthrange(begin_date.year, begin_date.month)[1])
        remaining_days_curr_month = num_days_begin_date_month - begin_date.day
        
        availability_string = availability_calendar.get('availability').get('unitAvailabilityConfiguration').get('availability')
        available_days_curr_month = availability_string[:remaining_days_curr_month].count('Y')
        availability[begin_date.strftime('%B')] = available_days_curr_month

        checkInAvailability_string = availability_calendar.get('availability').get('unitAvailabilityConfiguration').get('checkInAvailability')
        checkInAvailable_days_curr_month = checkInAvailability_string[:remaining_days_curr_month].count('Y')
        checkInAvailability[begin_date.strftime('%B')] = checkInAvailable_days_curr_month

        days_offset = days_offset + remaining_days_curr_month

        # current year
        for m in range(begin_date.month + 1, 13):
            month = datetime.date(begin_date.year, m, 1)
            num_days_month = monthrange(begin_date.year, m)[1]
            available_days_month = availability_string[days_offset:days_offset+num_days_month].count('Y')
            availability[month.strftime('%B')+str(month.year)] = available_days_month
            checkInAvailable_days_month = checkInAvailability_string[days_offset:days_offset+num_days_month].count('Y')
            checkInAvailability[month.strftime('%B')+str(month.year)] = checkInAvailable_days_month
            days_offset = days_offset + available_days_month

        # next year
        for m in range(1, 13):
            month = datetime.date(begin_date.year + 1, m, 1)
            num_days_month = monthrange(begin_date.year + 1, m)[1]
            available_days_month = availability_string[days_offset:days_offset+num_days_month].count('Y')
            availability[month.strftime('%B')+str(month.year)] = available_days_month
            checkInAvailable_days_month = checkInAvailability_string[days_offset:days_offset+num_days_month].count('Y')
            checkInAvailability[month.strftime('%B')+str(month.year)] = checkInAvailable_days_month
            days_offset = days_offset + available_days_month

        listing['availability'] = availability

        listing['checkInAvailability'] = checkInAvailability
                                      
        yield listing