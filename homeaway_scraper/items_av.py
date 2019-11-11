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
    availability = scrapy.Field()
    availability_calendar = scrapy.Field()
    checkInAvailability = scrapy.Field()