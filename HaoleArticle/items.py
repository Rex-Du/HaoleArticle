# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticleItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    content_html = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
        insert into haolearticle(title, content_html) 
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE title=VALUES(title),content_html=VALUES(content_html)
        """
        # 这里做这些处理是因为用itemloader得到的item的值都是list的，所以要做转换
        title = self['title']
        content_html = self['content_html']
        values = (title, content_html)
        return insert_sql, values


# class GebiarticleItem(scrapy.Item):
#     # define the fields for your item here like:
#     title = scrapy.Field()
#     content_html = scrapy.Field()
#
#     def get_insert_sql(self):
#         insert_sql = """
#         insert into haolearticle(title, content_html)
#         VALUES (%s, %s)
#         ON DUPLICATE KEY UPDATE title=VALUES(title),content_html=VALUES(content_html)
#         """
#         # 这里做这些处理是因为用itemloader得到的item的值都是list的，所以要做转换
#         title = self['title']
#         content_html = self['content_html']
#         values = (title, content_html)
#         return insert_sql, values