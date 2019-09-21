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
execute(['scrapy', 'crawl', 'gebi'])
execute(['scrapy', 'crawl', 'haole'])

