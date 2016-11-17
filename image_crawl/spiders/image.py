# -*- coding: utf-8 -*-

import re
import time
import urllib
# import urlparse
from urlparse import *
from selenium import webdriver
from scrapy.spiders import Spider,CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request,FormRequest
from image_crawl.items import ImageCrawlItem
from image_crawl.utils.select_result import *

class ImageSpider(Spider):
# class ImageSpider(CrawlSpider):
	name = "image"
	allowed_domains = ["zhihu.com"]
	# allowed_domains = ["zhihu.com","duitang.com"]
	# start_urls = ('http://rs.xidian.edu.cn/forum.php',)
	start_urls = ['https://www.zhihu.com/explore']
	# start_urls = ['https://www.zhihu.com/','http://www.duitang.com/']
	# rules = (
 #        # Extract links matching 'category.php' (but not matching 'subsection.php')
 #        # and follow links from them (since no callback means follow=True by default).
 #        # Rule(LinkExtractor(allow=('category\.php', ), deny=('subsection\.php', ))),
 #        # Extract links matching 'item.php' and parse them with the spider's method parse_item
 #        # Rule(LinkExtractor(restrict_xpaths=('//a')), callback='parse_item'),
 #        # Rule(LinkExtractor(restrict_xpaths=('//a[re:test(@href,.*javascript)]')), callback='parse'),
 #    )

	zhihu_headers = {
		"Accept": "*/*",
		"Accept-Encoding": "gzip,deflate",
		"Accept-Language": "en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4",
		"Connection": "keep-alive",
		"Content-Type":" application/x-www-form-urlencoded; charset=UTF-8",
		"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
		"Referer": "http://www.zhihu.com/"
	}

	#重写了爬虫类的方法, 实现了自定义请求, 运行成功后会调用callback回调函数
	def start_requests(self):
   		return [Request("https://www.zhihu.com/#signin", meta = {'cookiejar' : 1}, callback = self.post_login)]  #添加了meta

   #FormRequeset出问题了
	def post_login(self, response):
		print 'Preparing login'
       #下面这句话用于抓取请求网页后返回网页中的_xsrf字段的文字, 用于成功提交表单
		xsrf = response.xpath('//input[@name="_xsrf"]/@value').extract()[0]
		print xsrf
		#FormRequeset.from_response是Scrapy提供的一个函数, 用于post表单
		#登陆成功后, 会调用after_login回调函数
		return [FormRequest.from_response(response,   #"https://www.zhihu.com/#signin",
				meta = {'cookiejar' : response.meta['cookiejar']}, #注意这里cookie的获取
				headers = self.zhihu_headers,
				formdata = {
					'_xsrf': xsrf,
					'email': 'zhiyizhifeng@126.com',
					'password': '199341chenlei'
				},
				callback = self.after_login,
				dont_filter = True
			)]

	def after_login(self, response) :
		for url in self.start_urls :
			yield self.make_requests_from_url(url)

	def parse(self, response):
		response_selector = Selector(text=response.body)
		urlparse_scheme = urlparse(response.url)

		image_whole_url_list = []
		image_relative_url_list = response_selector.xpath('//img/@src').extract()

		internal_style_list = response.xpath('//style[@type="text/css"]').extract()
		for style in internal_style_list:
			if not style.find('url'):
				pass
			else:
				pattern=r'background.+url\((.+?)\)'
				internal_style_image_list=re.findall(pattern,style)
				image_relative_url_list.extend(internal_style_image_list)

		external_style_list = response.xpath('//link[@rel="stylesheet"]/@href').extract()
		for css_link in external_style_list:
		    whole_url=urljoin(urlparse_scheme.scheme+'://'+urlparse_scheme.netloc,css_link) if not css_link.startswith('http') else css_link
		    content=urllib.urlopen(whole_url).read()
		    if not content.find('url'):
		    	pass
		    else:
			    pattern=r'background.+url\((.+?)\)'
			    external_style_image_list=re.findall(pattern,content)
			    for i in external_style_image_list:
		    		image_relative_url_list.append(urljoin(whole_url,i))

		for relative_url in image_relative_url_list:
			if not relative_url.startswith('http'):
				whole_url = urljoin(urlparse_scheme.scheme + '://' + urlparse_scheme.netloc,relative_url)
				image_whole_url_list.append(whole_url)
			else:
				image_whole_url_list.append(relative_url)

		item = ImageCrawlItem()

		item['image_urls'] = image_whole_url_list
		item['origin_page_url']= response.url

		yield item

		a_links = response.xpath('//a/@href').extract()
		a_js_links = response.xpath('//a[re:test(@href,".*javascript")]/@href').extract()
		a_anchor_links = response.xpath('//a[re:test(@href,"^#")]/@href').extract()

		def filter_func(x):
			return x not in (a_js_links or a_anchor_links)

		# a_goto_links = response.xpath('//a/@href').extract()
		a_goto_links = filter(filter_func,a_links)

		for each_link in a_goto_links:
			if each_link:
				if not each_link.startswith('http'):
					whole_a_url = urljoin(urlparse_scheme.scheme + '://' + urlparse_scheme.netloc,each_link)
				yield Request(whole_a_url,callback=self.parse)