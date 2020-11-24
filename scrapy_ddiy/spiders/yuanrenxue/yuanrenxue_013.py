# -*- coding: utf-8 -*-
import re
import json
from scrapy import Request
from scrapy_ddiy.utils.spiders.ddiy_base import DdiyBaseSpider


class Yuanrenxue013(DdiyBaseSpider):
    name = 'yuanrenxue_013'
    description = '猿人学刷题平台-第13题入门级cookie'
    # 总价
    total_price = 0
    custom_settings = {'COOKIES_ENABLED': True}

    def start_requests(self):
        url = 'http://match.yuanrenxue.com/match/13'
        yield Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        headers = {'User-Agent': 'yuanrenxue.project'}
        cookie = re.search("document\\.cookie.*?=.*?\\(.*?\\+'", response.text).group()
        cookie = ''.join(re.findall("\\('(.)'\\)", cookie))
        k, v = cookie.split('=', maxsplit=1)
        cookie = {k: v}
        # 因为只有 5 页，故不必担心 cookie 过期问题
        for i in range(1, 6):
            url = f'http://match.yuanrenxue.com/api/match/13?page={i}'
            yield Request(url=url, cookies=cookie, headers=headers, callback=self.parse_page)

    def parse_page(self, response, **kwargs):
        data = json.loads(response.text).get('data')
        num_li = [i.get('value') for i in data]
        self.logger.info(num_li)
        self.total_price += sum(num_li)

    def closed(self, reason):
        self.logger.info(f'总价为：{self.total_price}')
        super().closed(reason)
