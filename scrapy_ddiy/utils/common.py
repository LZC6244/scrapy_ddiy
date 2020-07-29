# -*- coding: utf-8 -*-
import hashlib
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
