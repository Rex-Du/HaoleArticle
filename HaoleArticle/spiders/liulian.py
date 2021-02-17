# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy.http import Request

from HaoleArticle.items import ArticleItem


class HaoleSpider(scrapy.Spider):
    name = 'liulian'
    allowed_domains = ['www.llsp11.com']
    start_urls = [
        'https://www.llsp11.com/index.php/art/type/id/17',
        'https://www.llsp11.com/index.php/art/type/id/18',
        'https://www.llsp11.com/index.php/art/type/id/20',
        'https://www.llsp11.com/index.php/art/type/id/21',
        'https://www.llsp11.com/index.php/art/type/id/22',
        'https://www.llsp11.com/index.php/art/type/id/23',
        'https://www.llsp11.com/index.php/art/type/id/24',
        'https://www.llsp11.com/index.php/art/type/id/25',
    ]
    url_home = 'https://www.llsp11.com'
    next_urls = []

    def parse(self, response):
        detail_page_urls = response.xpath('//ul/li/a/@href').extract()
        for detail_page in detail_page_urls:
            detail_page_url = self.url_home + detail_page
            yield Request(url=detail_page_url, callback=self.parse_detail_url)

        next_page_url = response.xpath('//div[@class="page_info"]/a[@title="下一页"]/@href')
        next_page_url = self.url_home + next_page_url.extract_first() if next_page_url else None
        if next_page_url and next_page_url not in self.next_urls:
            self.next_urls.append(next_page_url)
            yield Request(url=next_page_url, callback=self.parse)

    def parse_detail_url(self, response):
        title = response.xpath('//div[@class="news_details"]/h1[@class="text-overflow"]/text()').extract_first()
        content_html = response.xpath('//div[@class="details-content text-justify"]').extract()
        if title and content_html:
            haole_item = ArticleItem()
            haole_item['title'] = title
            haole_item['content_html'] = content_html
            haole_item['platform'] = 'liulian'
            haole_item['platform_url'] = self.url_home
            yield haole_item
