# -*- coding: utf-8 -*-
import os
import re
import sys
import json
import base64
import ddddocr
import requests
from PIL import Image
from io import BytesIO
from threading import Lock
from scrapy import Selector
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
from scrapy_ddiy.utils.common import get_redis_conn
from scrapy_ddiy.utils.project import get_project_settings

TOTAL_TASKS = 1000
lock_glided_sky_011 = Lock()


def glided_sky_011():
    """
    GlidedSky 雪碧图2 爬虫
    为什么不使用 scrapy ：爬虫简易起见，ocr 图片转数字未搭建成服务可以接口形式使用，使用 scrapy 将阻塞
    ddddocr 识别数字时会 warning ：Expected shape from model of {1,19} does not match actual shape of ... 无需理会
    毕竟使用验证码识别库来识别数字本身就是一种取巧的办法 = =
    :return:
    """
    # 获取 cookie
    settings = get_project_settings()
    redis_conn = get_redis_conn(settings)
    cookies = {'glidedsky_session': redis_conn.get('glided_sky_cookie').decode()}
    redis_conn.close()

    all_number = dict()
    total = 0

    executor = ThreadPoolExecutor(max_workers=10)
    for i in range(1, 1001):
        url = f'http://glidedsky.com/level/web/crawler-sprite-image-2?page={i}'
        executor.submit(sprite_02, url, i, cookies, all_number)
    executor.shutdown(wait=True)
    file_name = 'glided_sky_011.json'
    with open(file_name, 'w') as f:
        json.dump(all_number, f, ensure_ascii=False)
    print(f'[{file_name}] 保存完毕')
    for li in all_number.values():
        total += sum(li)
    print(f'Sum or web number is {total}')


def sprite_02(url, page_num, cookies, all_number: dict):
    num_s_d = defaultdict(int)
    # 对同一页面进行多次请求，防止 ocr 识别错误
    # 出现重复识别结果即认为该页面识别正确
    while True:
        all_num_li = []
        r = requests.get(url=url, cookies=cookies)
        sel = Selector(text=r.text, type='html')

        if '/login' in r.url or '/login' in sel.xpath('//title/text()').get(''):
            warn_msg = f'[{url}] cookie 过期'
            print(warn_msg)
            sys.exit(-1)

        sprite_map = defaultdict(dict)
        style = sel.xpath('//style/text()').get()
        for i, j, k in re.findall('\\.([a-zA-Z0-9]+) \\{ ([a-zA-Z0-9-]+):-?(\\d+)px \\}', style):
            sprite_map[i][j] = int(k)
        # 获取雪碧图 base64 图片
        sprite_img = re.search('data:image/png;base64,([0-9a-zA-Z+/]+=*)', style).group(1)
        img = Image.open(BytesIO(base64.b64decode(sprite_img)))

        real_num_li = sel.xpath('//div[@class="col-md-1"]')

        for real_num in real_num_li:
            tmp_num_li = []
            div_num_li = real_num.xpath('.//div[contains(@class," sprite")]/@class').getall()
            for div_num in div_num_li:
                # 去除 ' sprite'
                div_num = div_num[:-7]
                # The crop rectangle, as a (left, upper, right, lower)-tuple.
                crop_img = img.crop((
                    sprite_map[div_num]['background-position-x'],
                    sprite_map[div_num]['background-position-y'],
                    sprite_map[div_num]['background-position-x'] + sprite_map[div_num]['width'],
                    sprite_map[div_num]['background-position-y'] + sprite_map[div_num]['height']
                ))
                # 将每张数字图片重设为 20x20 px
                crop_img = crop_img.resize(size=(20, 20))
                tmp_num_li.append(crop_img)
            real_num_img = Image.new('RGB', (20 * len(tmp_num_li), 20 * 1))
            for i, tmp_img in enumerate(tmp_num_li):
                real_num_img.paste(tmp_img, (20 * i, 0))
            bytes_io = BytesIO()
            real_num_img.save(bytes_io, format='png')
            ocr = ddddocr.DdddOcr()
            tmp_num = ocr.classification(bytes_io.getvalue())
            try:
                # ddddocr 是一个用于识别验证码的库，识别结果并不一定是数字
                # 对于本题来说非数字结果肯定是不对的
                # 此时应对本页面进行重新请求，使得网站更新雪碧图以识别数字
                all_num_li.append(int(tmp_num))
            except Exception as e:
                all_num_li.clear()
                break
        if not all_num_li:
            continue
        num_s = json.dumps(all_num_li)
        num_s_d[num_s] += 1
        if num_s_d[num_s] >= 5:
            # 多次请求同一页面多次，确保识别结果正确（此处同一识别结果出现 5 次即认为正确）
            global TOTAL_TASKS, lock_glided_sky_011
            with lock_glided_sky_011:
                TOTAL_TASKS -= 1
                print(f'[{1000 - TOTAL_TASKS}/1000] [{url}] => {all_num_li}')
                all_number[page_num] = all_num_li
            return all_num_li


if __name__ == '__main__':
    glided_sky_011()
