# -*- coding: utf-8 -*-
# @Author: lzc
# @Time  : 2020/6/15
# @Github: https://github.com/LZC6244
# @Desc  : 启动、运行爬虫
import os
import logging
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
from scrapy import cmdline
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings


def custom_log(settings, spider_name):
    """
    自定义日志文件
    :param settings: scrapy 项目配置
    :param spider_name: 爬虫名
    :return:
    """
    # 禁用 scrapy 自带日志配置
    configure_logging(install_root_handler=False)
    log_level = settings.get('LOG_LEVEL', logging.DEBUG)
    now = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    log_file_name = f'{settings.get("LOG_DIR")}/{spider_name}_{now}_{os.getpid()}.log'
    hdlr = TimedRotatingFileHandler(filename=log_file_name, when='midnight', interval=1)
    logging.basicConfig(handlers=[hdlr], level=log_level)


def main():
    settings = get_project_settings()
    custom_log(settings, 'base')
    cmdline.execute('scrapy crawl base'.split())


if __name__ == '__main__':
    main()
