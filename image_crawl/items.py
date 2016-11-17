# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ImageCrawlItem(scrapy.Item):
    # image_url = scrapy.Field() #image download url
    # image_name = scrapy.Field() # image stored name using SHA1()
    # image_id = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    origin_page_url = scrapy.Field() # page url which contains image