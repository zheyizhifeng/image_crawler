# -*- coding: utf-8 -*-

# Scrapy settings for image_crawl project
import os

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))

BOT_NAME = 'image_crawl'

SPIDER_MODULES = ['image_crawl.spiders']
NEWSPIDER_MODULE = 'image_crawl.spiders'


CONCURRENT_REQUESTS = 32
CONCURRENT_REQUESTS_PER_DOMAIN = 32

CONCURRENT_ITEMS = 100


DEPTH_LIMIT = 0
DEPTH_PRIORITY = 0
DNSCACHE_ENABLED = True

AUTOTHROTTLE_ENABLED = False
AUTOTHROTTLE_START_DELAY = 3.0
AUTOTHROTTLE_CONCURRENCY_CHECK_PERIOD = 10#How many


DOWNLOAD_DELAY = 0
CRAWLERA_PRESERVE_DELAY = True

#COOKIES_ENABLED=False
COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED=False

DOWNLOADER_MIDDLEWARES = {
   	'image_crawl.contrib.downloadmiddleware.google_cache.GoogleCacheMiddleware':50,
   	'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
   	'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': 200,
    'image_crawl.contrib.downloadmiddleware.rotate_useragent.RotateUserAgentMiddleware':400,
    'scrapy_crawlera.CrawleraMiddleware': 600
}
DEFAULT_REQUEST_HEADERS = {
  # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
  # 'Accept-Language': 'zh-CN,zh;q=0.8',
  'X-Crawlera-Cookies': 'disable'
}
USER_AGENT = ""

IMAGES_EXPIRES = 0
IMAGES_THUMBS = {
     'small': (50, 50),
     'big': (270, 270),
}
IMAGES_MIN_HEIGHT = 100
IMAGES_MIN_WIDTH = 100

ITEM_PIPELINES = {
   'scrapy.pipelines.images.ImagesPipeline': 1,
   'image_crawl.pipelines.ImageCrawlPipeline': 200,
   'scrapy_redis.pipelines.RedisPipeline': 200,
   'image_crawl.MongoPipeline.MongoPipeline': 400
}
IMAGES_STORE = os.path.join(PROJECT_DIR,'../images')


LOG_FILE = "logs/scrapy.log"

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED=True
#HTTPCACHE_EXPIRATION_SECS=0
#HTTPCACHE_DIR='httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES=[]
#HTTPCACHE_STORAGE='scrapy.contrib.httpcache.FilesystemCacheStorage'

MONGO_URI='127.0.0.1:27017'
MONGO_DATABASE='images'

REDIS_HOST='127.0.0.1'
REDIS_PORT='6379'

STATS_KEY = 'image:stats'

STATS_CLASS = 'image_crawl.statscol.graphite.RedisGraphiteStatsCollector'
GRAPHITE_HOST = '127.0.0.1'
GRAPHITE_PORT = 2003

CRAWLERA_ENABLED = True
CRAWLERA_USER = 'c3de7bf900c24eedb8a99564756a7260'
CRAWLERA_PASS = ''

SCHEDULER = "image_crawl.scrapy_redis.scheduler.Scheduler"
SCHEDULER_PERSIST = True
SCHEDULER_QUEUE_CLASS = 'image_crawl.scrapy_redis.queue.SpiderPriorityQueue'
