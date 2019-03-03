# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose


class BookItem(scrapy.Item):
    title = scrapy.Field()
    text = scrapy.Field()
    url = scrapy.Field()


class BooksItemLoader(ItemLoader):
    url_out = TakeFirst()

   # url_out = MapCompose(lambda x: x.lower())
