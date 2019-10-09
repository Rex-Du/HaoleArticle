"""
yibuo: 
"""
# Author     : rexdu
# FileName   : yibuo.py
# CreateDate : 2019-10-09 22:58

# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request

from HaoleArticle.items import ArticleItem


class GebiSpider(scrapy.Spider):
    name = 'yibuo'
    allowed_domains = ['yibuo.com']
    start_urls = [
        'http://yibuo.com/html/part/index51.html',
        'http://yibuo.com/html/part/index52.html',
        'http://yibuo.com/html/part/index53.html',
        'http://yibuo.com/html/part/index54.html',
        'http://yibuo.com/html/part/index55.html',
        'http://yibuo.com/html/part/index56.html',
        'http://yibuo.com/html/part/index57.html',
        'http://yibuo.com/html/part/index58.html',
    ]
    url_home = 'http://yibuo.com'
    next_urls = []

    def parse(self, response):
        # /html/body/div[9]/div/ul/li[2]/a
        detail_page_urls = response.xpath('//*[@class="box list channel"]/ul/li/a/@href').extract()
        for detail_page in detail_page_urls:
            detail_page_url = self.url_home + detail_page
            yield Request(url=detail_page_url, callback=self.parse_detail_url)

        # /html/body/div[9]/div/div[2]/a[10]
        next_page_urls = response.xpath('//div[@class="pagination"]/a/@href').extract()
        next_page_url = self.url_home + next_page_urls[-2] if len(next_page_urls)>2 else None
        if next_page_url:
            if next_page_url not in self.next_urls:
                self.next_urls.append(next_page_url)
                yield Request(url=next_page_url, callback=self.parse)

    def parse_detail_url(self, response):
        title = response.xpath('//div[@class="page_title"]/text()').extract_first()
        content_html = response.xpath('//div[@class="content"]').extract()
        if title and content_html:
            haole_item = ArticleItem()
            haole_item['title'] = title
            haole_item['content_html'] = content_html
            haole_item['platform'] = 'yibuo'
            haole_item['platform_url'] = self.url_home
            yield haole_item
        else:
            if not title:
                print('no title')


