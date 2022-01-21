# -*- coding: utf-8 -*-
import json
import subprocess
from scrapy import Request
from scrapy_ddiy import DdiyBaseSpider


def get_m():
    """获取加密参数m"""
    return subprocess.check_output(['node', 'scrapy_ddiy/scripts/js/yuanrenxue/002.js']).decode().strip()


class Yuanrenxue002(DdiyBaseSpider):
    name = 'yuanrenxue_002'
    description = '猿人学刷题平台-第2题js混淆 动态cookie'
    # 总价
    total_price = 0
    custom_settings = {'COOKIES_ENABLED': True}

    def start_requests(self):
        headers = {'User-Agent': 'yuanrenxue.project'}
        k, v = get_m().split('=', maxsplit=1)
        cookie = {k: v}
        for i in range(1, 6):
            url = f'http://match.yuanrenxue.com/api/match/2?page={i}'
            yield Request(url=url, headers=headers, cookies=cookie, callback=self.parse)

    def parse(self, response, **kwargs):
        data = json.loads(response.text).get('data')
        num_li = [i.get('value') for i in data]
        self.logger.info(num_li)
        self.total_price += sum(num_li)

    def closed(self, reason):
        self.logger.info(f'总价为：{self.total_price}')
        super().closed(reason)
