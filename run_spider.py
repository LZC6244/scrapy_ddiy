# -*- coding: utf-8 -*-
"""
启动、运行爬虫
"""
import os
import sys
from scrapy.exceptions import UsageError
from scrapy.utils.conf import arglist_to_dict
from scrapy.utils.project import get_project_settings
from scrapy_ddiy.utils.crawler import CustomCrawlerProcess
from scrapy_ddiy.utils.project import get_project_settings


def run_spider(spider_name, install_root_handler: bool = True, **kwargs):
    os.chdir(os.path.normpath(os.path.dirname(__file__)))
    settings = get_project_settings()
    process = CustomCrawlerProcess(settings, install_root_handler)
    process.crawl(spider_name, **kwargs)
    process.start()


if __name__ == '__main__':
    # 程序运行时传过来的参数
    run_arg_li = sys.argv
    # 爬虫启动时的附加参数
    spider_arg_li = []
    if len(run_arg_li) == 2:
        run_spider(run_arg_li[1])
    elif len(run_arg_li) > 2:
        for arg in run_arg_li[2:]:
            if arg == '-a':
                continue
            spider_arg_li.append(arg.strip('\'"'))
        try:
            spider_add_option: dict = arglist_to_dict(spider_arg_li)
        except Exception as e:
            raise UsageError('Invalid -a value, use like "-a NAME=VALUE -a NAME=VALUE ..."')
        run_spider(run_arg_li[1], **spider_add_option)
    else:
        run_spider('demo_spider')
