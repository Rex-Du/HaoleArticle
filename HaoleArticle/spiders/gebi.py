# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request

from HaoleArticle.items import ArticleItem


class GebiSpider(scrapy.Spider):
    name = 'gebi'
    allowed_domains = ['www.gebi43.com']
    start_urls = [
        'http://www.gebi43.com/arttype/29.html',
        'http://www.gebi43.com/arttype/30.html',
        'http://www.gebi43.com/arttype/31.html',
        'http://www.gebi43.com/arttype/32.html',
    ]
    url_home = 'http://www.gebi43.com'
    next_urls = []

    def parse(self, response):
        # //*[@id="main-content"]/main/table[1]/tbody/tr/td[1]/a
        # //*[@id="main-content"]/main/table[4]/tbody/tr/td[1]/a
        # //*[@id="main-content"]/main/table[1]/tbody/tr/td[1]/a
        detail_page_urls = response.xpath('//*[@id="main-content"]//td/a/@href').extract()
        title = response.xpath('//*[@id="main-content"]//td/a/text()').extract_first()
        for detail_page in detail_page_urls:
            detail_page_url = self.url_home + detail_page
            yield Request(url=detail_page_url, callback=self.parse_detail_url, meta={'title': title})

        # //*[@id="pager"]/li[8]/a
        # //*[@id="pager"]/li[8]/a
        next_page_url = response.xpath('//*[@id="pager"]/li[8]/a/@href')
        next_page_url = self.url_home + next_page_url.extract_first() if next_page_url else None
        if next_page_url:
            if next_page_url not in self.next_urls:
                self.next_urls.append(next_page_url)
                yield Request(url=next_page_url, callback=self.parse)

    def parse_detail_url(self, response):
        title = response.meta.get('title')
        content_html = response.xpath('//*[@id="main-content"]').extract()
        if title and content_html:
            haole_item = ArticleItem()
            haole_item['title'] = title
            haole_item['content_html'] = content_html
            yield haole_item