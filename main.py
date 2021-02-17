"""
main: 
"""
# Author     : rexdu
# FileName   : main.py
# CreateDate : 2019-09-21 10:10
"""
因为pycharm不支持scrapy项目的调试，这里新建一个main文件，模拟命令行执行scrapy命令
"""
import sys
import os

from scrapy.cmdline import execute


sys.path.append(os.path.basename(os.path.abspath(__file__)))
# execute(['scrapy', 'crawl', 'gebi'])
# execute(['scrapy', 'crawl', 'haole'])
# execute(['scrapy', 'crawl', 'yibuo'])
execute(['scrapy', 'crawl', 'liulian'])

# coding=utf8
# -*- coding: utf-8 -*-
# import os
#
# # 必须先加载项目settings配置
# # project需要改为你的工程名字（即settings.py所在的目录名字）
# os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'HaoleArticle.settings')
# from scrapy.crawler import CrawlerProcess
# from scrapy.utils.project import get_project_settings
#
# process = CrawlerProcess(get_project_settings())
# # 指定多个spider
# # process.crawl("gebi")
# # process.crawl("haole")
# process.crawl("yibuo")
# # 执行所有 spider
# for spider_name in process.spider_loader.list():
#     process.crawl(spider_name)
# process.start()
