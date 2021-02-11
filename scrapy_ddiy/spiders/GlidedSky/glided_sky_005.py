# -*- coding: utf-8 -*-
import json
import hashlib
from time import sleep
from scrapy import Request
from datetime import datetime
from scrapy_ddiy.utils.spiders.ddiy_base import DdiyBaseSpider


class GlidedSky005Spider(DdiyBaseSpider):
    name = 'glided_sky_005'
    description = 'GlidedSky  JS-加密1'
    custom_settings = {
        'COOKIES_ENABLED': True,
        'CONCURRENT_REQUESTS': 1,
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_ddiy.spiders.GlidedSky.glided_sky_downloadmiddleware.GlidedSkyMiddleware': 589,
        },
    }
    num_count = 0

    @staticmethod
    def get_url(page_num):
        """
        复现网页 JS ，计算出请求 URL
        计算出来的 t sign 只能使用一次
        :param page_num: 页码
        :return: 当前页码对应的请求 URL ，如：
                 http://www.glidedsky.com/api/level/web/crawler-javascript-obfuscation-1/items?page=1&t=1612867430
                 &sign=466d49a9bbedbbdd773fe3ae035d7dcaacf42c98
        """
        # 时间戳，如：1612867430
        t = int(datetime.now().timestamp())
        string = f'Xr0Z-javascript-obfuscation-1{t}'
        md5_obj = hashlib.sha1()
        md5_obj.update(string.encode(encoding='utf-8'))
        sign = md5_obj.hexdigest()
        url = f'http://www.glidedsky.com/api/level/web/crawler-javascript-obfuscation-1/items?page={page_num}&t={t}&sign={sign}'
        return url

    def start_requests(self):
        start_url = self.get_url(page_num=1)
        yield Request(url=start_url, callback=self.parse, dont_filter=True, meta={'page_num': 1})

    def parse(self, response, **kwargs):
        page_num = response.meta['page_num']
        data = json.loads(response.text)
        if not data:
            # 获取数据失败时进行无限重试
            # 缺失数据将导致答题失败
            sleep(2)
            retry_url = self.get_url(page_num)
            self.logger.info(f'重试第 {page_num} 页')
            yield Request(url=retry_url, callback=self.parse, dont_filter=True, meta={'page_num': page_num})
            return

        num_li = data.get('items', [])
        self.num_count += sum(num_li)
        self.logger.info(f'[ page: {page_num} ] => {num_li}')
        page_num += 1
        if page_num > 1000:
            # 题目网页共 1000 页
            return
        # 在此处需要等待 2 秒，因为计算出来的 t sign 只能使用一次
        # t 是根据当前时间戳进行计算的（时间戳经测试不能与当前时间有较大误差，当前时间 -5s 的时间都会请求失败）
        sleep(2)
        next_url = self.get_url(page_num)
        yield Request(url=next_url, callback=self.parse, dont_filter=True, meta={'page_num': page_num})

    def closed(self, reason):
        self.logger.info(f'Sum or web number is {self.num_count}')
