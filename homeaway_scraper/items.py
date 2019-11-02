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
    listingId = scrapy.Field()
    detailPageUrl = scrapy.Field()
    propertyType = scrapy.Field()
    currencyUnits = scrapy.Field()
    priceValue = scrapy.Field()
    periodType = scrapy.Field()
    formattedAmount = scrapy.Field()
    bedLinenProvided = scrapy.Field()
    parkingAvailable = scrapy.Field()
    averageRating = scrapy.Field()
    reviewCount = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    headline = scrapy.Field()