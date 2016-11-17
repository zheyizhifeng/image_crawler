# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
from scrapy import log
from scrapy.http import Request
from scrapy.pipelines.images import ImagesPipeline
from image_crawl.utils.select_result import list_first_item
from scrapy.exceptions import DropItem

class ImageCrawlPipeline(ImagesPipeline):

    def process_item(self, item, spider):
        return item
        pass

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
        	# item['origin_page_url']= response.url
        	yield Request(image_url,callback='parse')

    def item_completed(self, results, item, info):
        # if self.LOG_FAILED_RESULTS:
        #     msg = '%s found errors proessing %s' % (self.__class__.__name__, item)
        #     for ok, value in results:
        #         if not ok:
        #             log.err(value, msg, spider=info.spider)

        # for each in item['images']:
        # 	if each['path']:
        # 		item['image_id'] = each.checksum

       	image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")

        return item
