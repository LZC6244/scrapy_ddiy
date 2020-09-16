# -*- coding: utf-8 -*-
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
