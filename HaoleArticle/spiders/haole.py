# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy.http import Request

from HaoleArticle.items import ArticleItem


class HaoleSpider(scrapy.Spider):
    name = 'haole'
    allowed_domains = ['se.haodd42.com']
    start_urls = [
        'https://se.haodd42.com/listhtml/11.html',
        'https://se.haodd42.com/listhtml/12.html',
        'https://se.haodd42.com/listhtml/13.html',
        'https://se.haodd42.com/listhtml/14.html',
        'https://se.haodd42.com/listhtml/15.html',
        'https://se.haodd42.com/listhtml/16.html',
        'https://se.haodd42.com/listhtml/17.html',
        'https://se.haodd42.com/listhtml/18.html',
        'https://se.haodd42.com/listhtml/19.html',
    ]
    url_home = 'https://se.haodd42.com'
    next_urls = []

    def parse(self, response):
        detail_page_urls = response.xpath('//ul/li/a/@href').extract()
        for detail_page in detail_page_urls:
            detail_page_url = self.url_home + detail_page
            yield Request(url=detail_page_url, callback=self.parse_detail_url)

        # /html/body/div[54]/div[3]/a[17]
        # /html/body/div[54]/div[3]/a[17]
        next_page_url = response.xpath('//div[@class="page"]/a[17]/@href')
        next_page_url = self.url_home + next_page_url.extract_first() if next_page_url else None
        if next_page_url:
            if next_page_url not in self.next_urls:
                self.next_urls.append(next_page_url)
                yield Request(url=next_page_url, callback=self.parse)

    def parse_detail_url(self, response):
        title = response.xpath('//div[@class="title"]/text()').extract_first()
        content_html = response.xpath('//div[@class="center margintop border clear main"]').extract()
        if title and content_html:
            haole_item = ArticleItem()
            haole_item['title'] = title
            haole_item['content_html'] = content_html
            haole_item['platform'] = 'haole'
            haole_item['platform_url'] = self.url_home
            yield haole_item