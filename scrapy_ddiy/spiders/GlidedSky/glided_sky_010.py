# -*- coding: utf-8 -*-
import os
import re
import sys
import json
import math
import random
import shutil
import base64
import requests
import subprocess
from urllib import parse
from scrapy import Selector
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
from scrapy_ddiy.utils.common import get_redis_conn
from scrapy_ddiy.utils.project import get_project_settings


def glided_sky_010():
    """
    GlidedSky 验证码1 爬虫
    为什么不使用 scrapy ：爬虫简易起见，yolo v5 未搭建成服务可以接口形式使用，使用 scrapy 将阻塞
    为什么不使用多线程：需要用到 yolo v5 目标检测，本机配置不足
    :return:
    """
    # 获取 cookie
    settings = get_project_settings()
    redis_conn = get_redis_conn(settings)
    cookies = {'glidedsky_session': redis_conn.get('glided_sky_cookie').decode()}
    redis_conn.close()

    total_num = 0
    retry_times = 0
    for i in range(1, 1001):
        while True:
            all_number = tc_slide(cookies=cookies, page_index=i)
            if all_number:
                retry_times = 0
                print(f'[page-{i}] 成功获取数据：{all_number}')
                break
            else:
                retry_times += 1
                print(f'[page-{i}] 获取数据失败 {retry_times} 次')
                if retry_times < 5:
                    return

        total_num += sum(all_number)
    print(f'Sum or web number is {total_num}')


def get_mouse_track(move_px):
    """
    生成滑块轨迹
    这个没做什么轨迹校验，故这里生成轨迹的方式就比较随意了
    若轨迹做了校验，可以使用人工滑动获取轨迹，然后加入噪声生成轨迹的方式
    """
    # 获取鼠标轨迹 [[x,y,time],[x_offset,y_offset,time],[x_offset,y_offset,time],...]
    start_point = [random.randint(30, 80), random.randint(280, 300), random.randint(5, 15)]
    track_li = [start_point, [1, 0, random.randint(30, 40)]]
    moved_px = 1
    while moved_px <= move_px:
        left_px = random.choice([-1, 1, 2])
        tract = [left_px, 0, random.randint(0, 10)]
        track_li.append(tract)
        moved_px += left_px
    return track_li


def tc_slide(cookies: dict, page_index: int = 1, captcha_dir='glided_sky_captcha_01', yolo_dir=r'D:\lzc\yolov5'):
    js_dir = os.path.join(os.path.dirname(__file__), '../../../scripts/js/gilded_sky/010')
    aid = 2005597573
    protocol = 'https'
    accver = 1
    showtype = 'popup'

    real_ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 ' \
              'Safari/537.36'
    ua = parse.quote(base64.b64encode(re.sub('[\u00ff-\uffff]+', '', real_ua).encode()).decode())
    noheader = 1
    fb = 1
    aged = 0
    enableAged = 0
    enableDarkMode = 0
    grayscale = 1
    clientype = 2
    cap_cd = ''
    uid = ''
    wxLang = ''
    lang = 'zh-CN'
    entry_url = f'http://www.glidedsky.com/level/web/crawler-captcha-1?page={page_index}'[:1000]
    entry_url_query = dict([i.split('=', 1) for i in parse.urlparse(entry_url).query.split('&')])
    page_index = entry_url_query['page']
    captcha_img_path = os.path.join(captcha_dir, f'{page_index}.png')
    os.makedirs(captcha_dir, exist_ok=True)
    elder_captcha = 0
    subsid = 1

    # 获取第一个sess
    url = f'https://t.captcha.qq.com/cap_union_prehandle?aid={aid}&protocol={protocol}&accver={accver}' \
          f'&showtype={showtype}&ua={ua}&noheader={noheader}&fb={fb}&aged={aged}&enableAged={enableAged}' \
          f'&enableDarkMode={enableDarkMode}&grayscale={grayscale}&clientype={clientype}&cap_cd={cap_cd}&uid={uid}' \
          f'&wxLang={wxLang}&lang={lang}&entry_url={entry_url}&elder_captcha={elder_captcha}&subsid={subsid}'
    r = requests.get(url)
    data = json.loads(r.text[1:-1])
    sess = data['sess']
    sid = data['sid']

    # 获取第二个sess
    url = f'https://t.captcha.qq.com/cap_union_new_show?aid={aid}&protocol={protocol}&accver={accver}' \
          f'&showtype={showtype}&ua={ua}&noheader={noheader}&fb={fb}&aged={aged}&enableAged={enableAged}' \
          f'&enableDarkMode={enableDarkMode}&grayscale={grayscale}&clientype={clientype}&sess={sess}&fwidth=0' \
          f'&sid={sid}&wxLang={wxLang}&tcScale=1&uid=&cap_cd={cap_cd}&subsid={subsid}'
    r = requests.get(url)
    data = json.loads(
        re.sub('([{,])(.*?):', '\\g<1>"\\g<2>":', re.search('window\\.captchaConfig=(\\{.*?\\});', r.text).group(1)))
    sess = data['sess']
    spt = data['spt']

    # 获取验证码图片
    print(f'开始请求验证码图片：{page_index}')
    url = f'https://t.captcha.qq.com/cap_union_new_getcapbysig?aid={aid}&sess={sess}&sid={sid}&img_index=1&subsid=1'
    r = requests.get(url)
    with open(captcha_img_path, 'wb') as f:
        f.write(r.content)
    print(f'[page-{page_index}] 验证码图片保存完毕：{captcha_img_path}')

    print(f'[page-{page_index}] 使用 yolo v5 识别滑块位置完成')
    # 识别结果路径
    result_dir = os.path.join(yolo_dir, f'runs/detect/captcha_1_{page_index}')
    if os.path.exists(result_dir):
        shutil.rmtree(result_dir, ignore_errors=True)
    cmd_li = ['python',
              os.path.join(yolo_dir, 'detect.py'),
              '--source',
              captcha_img_path,
              '--conf-thres',
              '0.25',
              '--save-txt',
              '--save-conf',
              '--weights',
              os.path.join(yolo_dir, 'runs/train/captcha_1/weights/best.pt'),
              '--name',
              f'captcha_1_{page_index}']
    cmd_result = subprocess.check_output(cmd_li, shell=True, stderr=subprocess.STDOUT).decode()
    cmd_result = re.sub('\x1b\\[\\dm', '', cmd_result).strip().split('\r\n')
    # 识别结果文件路径
    label_path = os.path.join(result_dir, f'labels/{page_index}.txt')
    with open(label_path, 'r') as f:
        content_li = [[float(j) for j in i.strip().split(' ')] for i in f.readlines()]
        # 根据置信度升序排序
        content_li.sort(key=lambda x: x[-1])
        # [class, x_center, y_center, width, height]
        content = content_li[-1]
        # 验证码整张图片固定 {top: 63.328125, left: 9.59375}
        # 滑块框和滑块缺口相距约20px
        # 滑块图片大小为 680x390 ，网页中缩放了50%，故其left中计算有个乘以2
        captcha_box_left = round((content[1] - content[3] / 2) * 680 - 20, 5)
        captcha_box_top = round((content[2] - content[4] / 2) * 390 - 20, 5)
        # 滑块需要移动的距离，初始位置为26
        move_px = math.ceil(captcha_box_left / 2 - 26 + random.randint(-3, 3))
    slide_value = get_mouse_track(move_px)
    # ft = subprocess.check_output(['node', os.path.join(js_dir, 'get_ft.js')], shell=True,
    #                              stderr=subprocess.STDOUT).decode().strip()
    # ft 暂时写死，补环境太麻烦了
    ft = 'qf_7P_n_H'

    # ans 滑块框最终位置， top 为 spt
    ans = f'{math.floor(captcha_box_left)},{math.floor(float(spt))};'
    collect, eks = subprocess.check_output(['node', os.path.join(js_dir, 'tdc.js'), json.dumps(slide_value), ft],
                                           shell=True,
                                           stderr=subprocess.STDOUT).decode().strip().split('\n')
    form_data = {
        'aid': aid,
        'protocol': protocol,
        'accver': accver,
        'showtype': showtype,
        'ua': ua,
        'noheader': noheader,
        'fb': fb,
        'aged': aged,
        'enableAged': enableAged,
        'enableDarkMode': enableDarkMode,
        'grayscale': grayscale,
        'clientype': clientype,
        'sess': sess,
        'fwidth': 0,
        'sid': sid,
        'wxLang': wxLang,
        'tcScale': 1,
        'uid': uid,
        'cap_cd': cap_cd,
        'prehandleLoadTime': random.randint(0, 20),
        'createIframeStart': int(datetime.now().timestamp() * 1000),
        'subsid': subsid,
        'cdata': 0,
        'ans': ans,
        'vsig': '',
        'websig': '',
        'subcapclass': '',
        # pow_answer 和 pow_calc_time 已完成抠出js计算，为简便此处pow_calc_time使用随机值
        # 'pow_answer': data['powCfg']['prefix'],
        'pow_calc_time': random.randint(5, 50),
        'collect': collect,
        'tlg': len(collect),
        'fpinfo': '',
        'eks': eks,
        'nonce': data['nonce'],
        'vlg': '0_0_1',
        # 'vData': '0_0_1',
    }
    r = requests.post(url='https://t.captcha.qq.com/cap_union_new_verify', data=form_data)
    data = r.json()
    randstr = data['randstr']
    ticket = data['ticket']

    url = f'{entry_url}&ticket={ticket}&rand_str={randstr}'
    # 可不带 headers
    headers = {
        'User-Agent': real_ua,
        'Referer': entry_url,
    }
    response = requests.get(url=url, cookies=cookies, headers=headers)
    sel = Selector(text=response.text)
    all_number = [int(i) for i in
                  sel.xpath('//div[@class="card-body"]//div[@class="col-md-1"]/text()').getall()]
    return all_number


if __name__ == '__main__':
    glided_sky_010()
