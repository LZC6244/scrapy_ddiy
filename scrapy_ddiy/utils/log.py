# -*- coding: utf-8 -*-
"""
@Author: lzc
@Time  : 2020/7/12
@Github: https://github.com/LZC6244
@Desc  : 根据 scrapy.utils.log 进行重写
"""
from scrapy.utils.log import *
from twisted.python import log as twisted_log
from logging.config import dictConfig
from logging.handlers import TimedRotatingFileHandler

DEFAULT_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'loggers': {
        'scrapy': {
            'level': 'DEBUG',
        },
        'twisted': {
            'level': 'ERROR',
        },
    }
}
_scrapy_root_handler = None


def custom_configure_logging(settings=None, install_root_handler=True, spider_name=None):
    if not sys.warnoptions:
        # Route warnings through python logging
        logging.captureWarnings(True)

    observer = twisted_log.PythonLoggingObserver('twisted')
    observer.start()

    dictConfig(DEFAULT_LOGGING)

    if isinstance(settings, dict) or settings is None:
        settings = Settings(settings)

    if settings.getbool('LOG_STDOUT'):
        sys.stdout = StreamLogger(logging.getLogger('stdout'))

    if install_root_handler:
        # install_scrapy_root_handler(settings)
        # 重写了这里，加入可以轮询的日志
        custom_install_scrapy_root_handler(settings, spider_name)


def custom_install_scrapy_root_handler(settings, spider_name):
    global _scrapy_root_handler

    if (_scrapy_root_handler is not None
            and _scrapy_root_handler in logging.root.handlers
            and not settings.getbool('LOG_TO_CONSOLE')):
        logging.root.removeHandler(_scrapy_root_handler)
    logging.root.setLevel(logging.NOTSET)
    _scrapy_root_handler = custom_get_handler(settings)
    logging.root.addHandler(_scrapy_root_handler)


def get_time_rotating_handler(settings):
    log_level = settings.get('LOG_LEVEL', logging.DEBUG)
    log_encoding = settings.get('LOG_ENCODING', 'utf-8')
    log_file = settings.get('LOG_FILE')
    if not log_file:
        raise ValueError('Please check the [ LOG_FILE ] attribute of settings.')
    log_rotating_cfg: dict = settings.get('LOG_ROTATING_CFG')
    handler = TimedRotatingFileHandler(filename=log_file, encoding=log_encoding, **log_rotating_cfg)
    handler.setLevel(log_level)
    return handler


def custom_get_scrapy_root_handler():
    return _scrapy_root_handler


def custom_get_handler(settings):
    """ Return a log handler object according to settings """
    filename = settings.get('LOG_FILE')
    if filename:
        encoding = settings.get('LOG_ENCODING')
        if settings.getbool('LOG_TIME_ROTATING'):
            handler = get_time_rotating_handler(settings)
        else:
            handler = logging.FileHandler(filename, encoding=encoding)
    elif settings.getbool('LOG_ENABLED'):
        handler = logging.StreamHandler()
    else:
        handler = logging.NullHandler()

    formatter = logging.Formatter(
        fmt=settings.get('LOG_FORMAT'),
        datefmt=settings.get('LOG_DATEFORMAT')
    )
    handler.setFormatter(formatter)
    handler.setLevel(settings.get('LOG_LEVEL'))
    if settings.getbool('LOG_SHORT_NAMES'):
        handler.addFilter(TopLevelFormatter(['scrapy']))
    return handler
