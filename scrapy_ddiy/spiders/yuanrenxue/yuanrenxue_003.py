# -*- coding: utf-8 -*-
import re
import json
from scrapy import Request
from scrapy_ddiy import DdiyBaseSpider


class Yuanrenxue003(DdiyBaseSpider):
    name = 'yuanrenxue_003'
    description = '猿人学刷题平台-第3题访问逻辑 推心置腹'
    # 总价
    total_price = 0
    custom_settings = {'COOKIES_ENABLED': True}
    headers = {
        'Host': 'match.yuanrenxue.com',
        'User-Agent': 'yuanrenxue.project',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Referer': 'http://match.yuanrenxue.com/match/3',
    }

    def start_requests(self):
        for i in range(1, 6):
            # 网站目标页数较少，可以直接使用 cookie 不必担心过期
            url = 'http://match.yuanrenxue.com/logo'
            yield Request(url=url, headers=self.headers, callback=self.get_cookie, dont_filter=True, priority=100,
                          meta={'page_num': i, 'dont_merge_cookies': True})

    def get_cookie(self, response):
        page_num = response.meta.get('page_num')
        cookie_s = response.headers.get(b'Set-Cookie').decode()
        if not cookie_s.endswith(';'):
            cookie_s += ';'
        cookie = dict([i.rstrip(';').split('=', maxsplit=1) for i in re.findall('[^\\s]+?=[^\\s]+?;', cookie_s)])
        sessionid = cookie.get('sessionid')

        url = f'http://match.yuanrenxue.com/api/match/3?page={page_num}'
        yield Request(url=url, headers=self.headers, callback=self.parse, priority=200,
                      cookies={'sessionid': sessionid})

    def parse(self, response, **kwargs):
        data = json.loads(response.text).get('data')
        num_li = [i.get('value') for i in data]
        self.logger.info(num_li)
        self.total_price += sum(num_li)

    def closed(self, reason):
        self.logger.info(f'总价为：{self.total_price}')
        super().closed(reason)
