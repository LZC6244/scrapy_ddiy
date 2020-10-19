# -*- coding: utf-8 -*-
import os
import re
import sys
import random
import requests
from scrapy import Selector
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
from scrapy_ddiy.utils.project import get_project_settings
from scrapy_ddiy.utils.common import run_func, get_redis_conn
from scrapy_ddiy.downloadermiddlewares.custom_user_agent import USER_AGENTS

GLIDED_SKY_COOKIE_SET_NAME = 'glided_sky_cookie'


def get_glided_sky_cookie(glided_sky_email: str = None, glided_sky_password: str = None):
    glided_sky_email = glided_sky_email or os.environ.get('GLIDED_SKY_EMAIL')
    glided_sky_password = glided_sky_password or os.environ.get('GLIDED_SKY_PASSWORD')
    home_url = 'http://www.glidedsky.com/'
    login_url = 'http://www.glidedsky.com/login'
    user_agent = random.choice(USER_AGENTS)
    session = requests.session()
    headers = {
        'Host': 'www.glidedsky.com',
        'User-Agent': user_agent,
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',

    }
    response = session.get(url=home_url, headers=headers)
    response_cookie = response.headers.get('Set-Cookie')
    xsrf_token = re.search('XSRF-TOKEN=(.*?);', response_cookie).group(1)
    glidedsky_session = re.search('glidedsky_session=(.*?);', response_cookie).group(1)
    # headers['Cookie'] = f'XSRF-TOKEN={token}'
    # headers['Referer'] = login_url
    # response = session.get(url=login_url, headers=headers)
    sel = Selector(text=response.text, type='html')
    token = sel.xpath('//meta[@name="csrf-token"]/@content').get()
    form_data = {
        '_token': token,
        'email': glided_sky_email,
        'password': glided_sky_password,
    }
    headers = {
        'Host': 'www.glidedsky.com',
        'User-Agent': user_agent,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'http://www.glidedsky.com',
        'Referer': 'http://www.glidedsky.com/login',
        'Cookie': f'XSRF-TOKEN={xsrf_token};glidedsky_session={glidedsky_session}',
        'Upgrade-Insecure-Requests': '1',
    }
    response = session.post(url=login_url, data=form_data, headers=headers)
    now = datetime.now()
    if response.status_code != 200 or '/login' in response.url:
        warn_msg = f'[{response.status_code}]Got GlidedSky failed.'
        print(f'{now} --> {warn_msg}')
        raise RuntimeError(warn_msg)
    response_cookie = response.headers.get('Set-Cookie')
    user_cookie = re.search('glidedsky_session=(.*?);', response_cookie).group(1)
    print(f'{now} --> Got GlidedSky cookie successful.')
    return user_cookie


def set_glided_sky_cookie_to_redis(glided_sky_email: str = None, glided_sky_password: str = None):
    redis_conn = get_redis_conn(get_project_settings())
    user_cookie = get_glided_sky_cookie(glided_sky_email, glided_sky_password)
    redis_conn.set(GLIDED_SKY_COOKIE_SET_NAME, user_cookie)
    redis_conn.close()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        run_func(sys.argv, locals())
    else:
        set_glided_sky_cookie_to_redis()
