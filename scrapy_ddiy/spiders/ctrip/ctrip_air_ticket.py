# -*- coding: utf-8 -*-
import os
import ast
import json
import random
import subprocess
from MsgBot import WxComBot
from datetime import datetime
from scrapy import FormRequest, Request
from scrapy_ddiy.utils.spiders import DdiyBaseSpider


class CtripAirTicket(DdiyBaseSpider):
    """
    运行方式如：
    1. 在run_spider脚本运行
    # [['出发地','目的地','出发日期如2022-01-30','低价预警如500']]
    run_spider('ctrip_air_ticket', trip_li=[['成都', '上海', '2022-01-28', 666]],agent_id='xxx', notice_wx_com='xxx')
    2. 命令行运行
    python run_spider.py ctrip_air_ticket -a trip_li="[['成都', '上海', '2022-01-28', 666]]" -a agent_id="xxx" -a notice_wx_com="xxx"
    """
    name = 'ctrip_air_ticket'
    description = '携程机票爬虫'
    custom_settings = {
        'COOKIES_ENABLED': True,
        'ITEM_PIPELINES': {
            'scrapy_ddiy.pipelines.mongodb.MongodbPipeline': 300,
        },
    }
    wx_com_bot: WxComBot
    agent_id: int
    notice_wx_com: str
    city_info = dict()
    time_fmt = '%Y-%m-%d %H:%M:%S'
    # 晚于 xx 点后航班无视
    before_hour: int = 21

    def custom_init(self, *args, **kwargs):
        env = os.environ
        self.agent_id = int(env.get('WX_COM_AGENT_ID'))
        self.wx_com_bot = WxComBot(corp_id=env.get('WX_COM_CORP_ID'), corp_secret=env.get('WX_COM_CORP_SECRET'))

        self.before_hour = int(self.before_hour)
        self.logger.info(f'before_hour is {self.before_hour}')

    def start_requests(self):
        trip_li = getattr(self, 'trip_li', None)
        if not trip_li:
            msg = "运行爬虫必须传参 [trip_li] 如：[['出发地','目的地','出发日期如2022-01-30']]"
            self.logger.error(msg)
            return []
        if isinstance(trip_li, str):
            trip_li = ast.literal_eval(trip_li)

        self.logger.info(f'trip_li is {trip_li}')
        self.trip_li = trip_li

        # 获取城市
        form_data = {"q": '1', "b": '3',
                     "head": {"ctok": "", "cver": "1.0", "lang": "01", "syscode": "09", "auth": None,
                              "extension": [{"name": "protocal", "value": "https"}]},
                     "contentType": "json"}
        url = 'https://m.ctrip.com/restapi/soa2/13515/airportCityList'
        yield FormRequest(url=url, body=json.dumps(form_data), method='POST', callback=self.parse, dont_filter=True)

    def parse(self, response, **kwargs):
        """获取城市名对应查询代码，并查询航班"""
        data = json.loads(response.text)
        # A-Z 城市列表
        pl = data.get('pl')
        if not pl:
            self.crawler.engine.close_spider(self, f'不存在 A-Z 城市列表数据 [pl] ，请检查\n原始响应如下\n{response.text}')
            return
        for p in pl:
            for c in p['cl']:
                self.city_info[c['name']] = c['code']

        url = 'https://m.ctrip.com/restapi/soa2/10290/createclientid?systemcode=09&createtype=3&head%5Bcid%5D=&' \
              'head%5Bctok%5D=&head%5Bcver%5D=1.0&head%5Blang%5D=01&head%5Bsid%5D=8888&head%5Bsyscode%5D=09&' \
              'head%5Bauth%5D=null&head%5Bextension%5D%5B0%5D%5Bname%5D=protocal&' \
              'head%5Bextension%5D%5B0%5D%5Bvalue%5D=https&contentType=json'
        yield Request(url=url, callback=self.parse_client_id, dont_filter=True)

    def parse_client_id(self, response):
        """
        获取 client_id （cid,guid），如：09031143412382051744
        cid 其实可以随便写（如1111,2222,...），这里为了复现生成过程进行获取
        """
        data = json.loads(response.text)
        cid = data.get('ClientID')
        if not cid:
            self.crawler.engine.close_spider(self, f'获取 cid 失败，请检查')
            return

        js_dir = os.path.join(os.path.dirname(__file__), '../../../scripts/js/ctrip')
        uuid = subprocess.check_output(['node', os.path.join(js_dir, 'get_uuid.js')],
                                       shell=True, stderr=subprocess.STDOUT).decode().strip().split('\n')
        uuid = uuid[0]
        self.logger.info(f'生成 uuid ：{uuid}')
        create_time = int(datetime.now().timestamp() * 1000) - random.randint(3e5, 4e5)
        post_time = create_time + random.randint(1e5, 2e5)
        vid = f'{create_time}.{uuid}'
        _bfa = f'1.{vid}.1.{create_time}.{post_time}.1.1.{random.randint(1e10, 1.1e10)}'
        self.logger.info(f'生成 _bfa ：{_bfa}')
        cookies = {'_bfa': _bfa}

        url = 'https://m.ctrip.com/restapi/soa2/14022/flightListSearch'
        for origin, dest, date, low_price in self.trip_li:
            origin_code = self.city_info[origin]
            dest_code = self.city_info[dest]
            form_data = {
                "preprdid": "", "trptpe": 1, "flag": 8,
                "searchitem": [{"dccode": origin_code, "accode": dest_code, "dtime": date}],
                "subchannel": None,
                "head": {"cid": cid, "ctok": "", "cver": "1.0", "lang": "01", "syscode": "09", "auth": None,
                         "extension": [{"name": "protocal", "value": "https"}]}
                ,
                "contentType": "json"
            }
            yield FormRequest(url=url, body=json.dumps(form_data), method='POST', cookies=cookies,
                              callback=self.parse_fright, meta={'low_price': low_price}, dont_filter=True)

    def parse_fright(self, response):
        """解析航班"""
        low_price = response.meta['low_price']
        data = json.loads(response.text)
        for flt in data['fltitem']:
            date_info = flt['mutilstn'][0]['dateinfo']
            # 起飞时间
            start_time = date_info['ddate']

            if datetime.strptime(start_time, self.time_fmt).hour >= self.before_hour:
                continue

            # 降落时间
            end_time = date_info['adate']
            # 航班号
            flight_name = flt['mutilstn'][0]['basinfo']['airsname'] + '-' + flt['mutilstn'][0]['basinfo']['flgno']
            price_li = [i['priceinfo'][0]['price'] for i in flt['policyinfo']]
            min_price = min(price_li)
            _id = f''
            item = {
                'flight_name': flight_name,
                'start_time': start_time,
                'end_time': end_time,
                'min_price': min_price,
            }
            # 不生成 _id ，使用 MongoDB自动生成的 ObjectId
            item = self.process_parsed_item(response=response, parsed_item=item, set_id=False)
            yield item

            if low_price >= min_price:
                msg = f'【携程】检测到低价机票\n' \
                      f'航班：{flight_name}\n' \
                      f'起飞时间：{start_time}\n' \
                      f'降落时间：{end_time}\n' \
                      f'当前票价：{min_price}\n' \
                      f'预警票价：{low_price}'
                self.wx_com_bot.send_msg_text(agent_id=self.agent_id, content=msg, to_user=self.notice_wx_com)