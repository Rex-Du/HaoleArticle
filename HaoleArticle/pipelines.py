# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from MySQLdb import cursors
from twisted.enterprise import adbapi  # 这个api可以装mysql的操作变成异步的操作


class HaolearticlePipeline(object):
    def process_item(self, item, spider):
        return item


class MysqlTwistedPipline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings['MYSQL_HOST'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWORD'],
            database=settings['MYSQL_DB'],
            charset=settings['MYSQL_CHARSET'],
            use_unicode=settings['MYSQL_USE_UNICODE']
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item)

    def handle_error(self, failure, item):
        print(failure)

    def do_insert(self, cursor, item):
        insert_sql, values = item.get_insert_sql()  # 这种写法就要求每个item类里必需要有get_insert_sql这个方法
        cursor.execute(insert_sql, values)
