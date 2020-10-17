# -*- coding: utf-8 -*-
import ast
import redis
import socket
import hashlib
import pymongo
from scrapy import Request
from w3lib.url import canonicalize_url
from scrapy.utils.python import to_bytes


def get_str_md5(string: str, encoding='utf-8'):
    """
    计算字符串的 MD5 值
    :param string:
    :param encoding:
    :return:
    """
    md5_obj = hashlib.md5()
    md5_obj.update(string.encode(encoding=encoding))
    return md5_obj.hexdigest()


def get_request_md5(request: Request):
    """
    计算 scrapy.Request 的 MD5 值
    （仿照 scrapy.utils.request 的 request_fingerprint 函数）
    :param request:
    :return:
    """
    md5_obj = hashlib.md5()
    md5_obj.update(to_bytes(request.method))
    md5_obj.update(to_bytes(canonicalize_url(request.url)))
    md5_obj.update(request.body or b'')
    return md5_obj.hexdigest()


def get_redis_conn(settings):
    """从项目配置中获取Redis配置并建立连接"""
    return redis.Redis(host=settings.get('REDIS_HOST'), port=settings.get('REDIS_PORT'),
                       **settings.get('REDIS_PARAMS'))


def get_mongo_cli(settings):
    """从项目配置中获取MongoDB配置并建立连接"""
    return pymongo.MongoClient(settings.get('MONGO_URI'), **settings.get('MONGO_PARAMS'))


def get_local_ip():
    """
    :return: 本地内网 IP 字符串,如：'192.168.0.1'
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    local_ip = s.getsockname()[0]
    s.close()
    return local_ip


def cookie_str_to_dict(cookie_str):
    """将浏览器抓包获取到的 cookie 字符串转换为字典形式"""
    cookie_dict = dict()
    for i in cookie_str.split(';'):
        i = i.strip()
        if '=' not in i:
            i += '='
        k, v = i.split('=', maxsplit=1)
        cookie_dict[k] = v
    return cookie_dict


def run_func(argv, local_var):
    """Run as : run_func(sys.argv, locals())"""
    argv_len = len(argv)
    warn_msg = f'Please run this program as [ python file_name.py function_name k1=v1 k2="\'str_v2\'" ... ] \n' \
               f'(Please use single quotes when passing strings)\n'
    if argv_len > 1:
        func_name = argv[1]
        func = local_var.get(func_name)
        assert func, f'Please check if [ {func_name} ] exists '
        params = dict()
        try:
            for arg in argv[2:]:
                k, v = arg.split('=', 1)
                v = v.strip("'") if v.startswith("'") else ast.literal_eval(v)
                params[k] = v
        except:
            raise UserWarning(warn_msg)
        return func(**params)
    else:
        print(warn_msg)
