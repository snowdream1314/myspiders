# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SecondSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class mgpyhItem(scrapy.Item):
    
    id = scrapy.Field()
    name = scrapy.Field()
    href = scrapy.Field()
    
    
from scrapy.item import Item, Field
  
class HnItem(Item):
    title = Field()
    link = Field()
    