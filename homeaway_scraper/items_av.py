# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HomeawayScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # Room fields
    propertyId = scrapy.Field()
    detailPageUrl = scrapy.Field()
    month = scrapy.Field()
    year = scrapy.Field()
    available_days = scrapy.Field()
    checkin_available_days = scrapy.Field()
    availabilityUpdated = scrapy.Field()
    #days_offset = scrapy.Field()
    #month_availability_string = scrapy.Field()
