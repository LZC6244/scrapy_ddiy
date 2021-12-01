# -*- coding: utf-8 -*-
from scrapy_ddiy.spiders.GlidedSky.glided_sky_003 import GlidedSky003Spider


class GlidedSky004Spider(GlidedSky003Spider):
    name = 'glided_sky_004'
    description = 'GlidedSky 爬虫-IP屏蔽2'
    start_url = 'http://www.glidedsky.com/level/web/crawler-ip-block-2'
