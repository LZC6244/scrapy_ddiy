# -*- coding: utf-8 -*-
import json
from scrapy import FormRequest
from scrapy_ddiy.utils.common import get_str_md5
from scrapy_ddiy.spiders.example_spiders.alapi.alapi_dog import AlapiDogSpider


class AlapiHitokotoSpider(AlapiDogSpider):
    name = 'alapi_hitokoto'
    description = 'ALAPI Hitokoto-一言'
    start_url = 'https://v1.alapi.cn/api/hitokoto'
    type_map: dict

    def custom_init(self, *args, **kwargs):
        self.type_map = {'a': '动画', 'b': '漫画', 'c': '游戏', 'd': '文学', 'e': '原创',
                         'f': '来自网络', 'g': '其他', 'h': '影视', 'i': '诗词', 'j': '网易云',
                         'k': '哲学', 'l': '抖机灵'}

    def start_requests(self):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        for i in range(8):
            for t in self.type_map.keys():
                form_data = {'format': 'json', 'type': t}
                yield FormRequest(url=self.start_url, callback=self.parse, dont_filter=True,
                                  headers=headers, formdata=form_data)

    def parse(self, response, **kwargs):
        if not self.check_status(response):
            return
        data = json.loads(response.text).get('data')
        content = data.get('hitokoto')
        from_s = data.get('from')
        creator_s = data.get('creator')
        type_s = self.type_map.get(data.get('type'))
        item = {'_id': get_str_md5(content), 'content': content, 'from': from_s,
                'creator': creator_s, 'type': type_s, 'sent_time': None}
        item = self.process_parsed_item(response, item)
        yield item
