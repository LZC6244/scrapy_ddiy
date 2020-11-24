# -*- coding: utf-8 -*-
import json
import base64
from urllib import parse
from scrapy import Request
from scrapy_ddiy.utils.spiders.ddiy_base import DdiyBaseSpider


class Yuanrenxue012(DdiyBaseSpider):
    name = 'yuanrenxue_012'
    description = '猿人学刷题平台-第12题入门级js'
    # 总价
    total_price = 0

    def start_requests(self):
        headers = {'User-Agent': 'yuanrenxue.project'}
        for i in range(1, 6):
            # 生成加密参数 m
            m = base64.b64encode(parse.quote(f'yuanrenxue{i}').encode()).decode()
            url = f'http://match.yuanrenxue.com/api/match/12?page={i}&m={m}'
            yield Request(url=url, headers=headers, callback=self.parse)

    def parse(self, response, **kwargs):
        data = json.loads(response.text).get('data')
        num_li = [i.get('value') for i in data]
        self.logger.info(num_li)
        self.total_price += sum(num_li)

    def closed(self, reason):
        self.logger.info(f'总价为：{self.total_price}')
        super().closed(reason)
