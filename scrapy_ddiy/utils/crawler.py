# -*- coding: utf-8 -*-
"""
根据 scrapy.utils.crawler 进行重写
"""
import six
import signal
import pprint
import logging
from twisted.internet import reactor
from typing import TYPE_CHECKING, Optional
from scrapy import Spider, signals
from scrapy.core.engine import ExecutionEngine
from scrapy.crawler import Crawler, CrawlerRunner
from scrapy.resolver import CachingThreadedResolver
from scrapy.utils.ossignal import install_shutdown_handlers, signal_names
from scrapy.settings import overridden_settings, Settings
from scrapy.signalmanager import SignalManager
from scrapy.utils.misc import create_instance, load_object
from scrapy.utils.reactor import (
    install_reactor,
    is_asyncio_reactor_installed,
    verify_installed_asyncio_event_loop,
    verify_installed_reactor,
)
from scrapy.utils.log import (
    LogCounterHandler,
    configure_logging,
    get_scrapy_root_handler,
    install_scrapy_root_handler,
    log_reactor_info,
    log_scrapy_info,
)
from scrapy.extension import ExtensionManager
from scrapy_ddiy.utils.log import custom_configure_logging
from scrapy_ddiy.utils.log import custom_install_scrapy_root_handler, custom_get_scrapy_root_handler

if TYPE_CHECKING:
    from scrapy.utils.request import RequestFingerprinter

logger = logging.getLogger(__name__)


class CustomCrawler(Crawler):
    """更改处为 custom_xx 函数"""

    def __init__(self, spidercls, settings=None, init_reactor: bool = False):
        if isinstance(spidercls, Spider):
            raise ValueError("The spidercls argument must be a class, not an object")

        if isinstance(settings, dict) or settings is None:
            settings = Settings(settings)

        self.spidercls = spidercls
        self.settings = settings.copy()
        self.spidercls.update_settings(self.settings)

        self.signals = SignalManager(self)

        self.stats = load_object(self.settings["STATS_CLASS"])(self)

        handler = LogCounterHandler(self, level=self.settings.get("LOG_LEVEL"))
        logging.root.addHandler(handler)

        d = dict(overridden_settings(self.settings))
        logger.info(
            "Overridden settings:\n%(settings)s", {"settings": pprint.pformat(d)}
        )

        # if get_scrapy_root_handler() is not None:
        if custom_get_scrapy_root_handler() is not None:
            # scrapy root handler already installed: update it with new settings
            # install_scrapy_root_handler(self.settings)
            custom_install_scrapy_root_handler(self.settings, spidercls.name)
        # lambda is assigned to Crawler attribute because this way it is not
        # garbage collected after leaving __init__ scope
        self.__remove_handler = lambda: logging.root.removeHandler(handler)
        self.signals.connect(self.__remove_handler, signals.engine_stopped)

        lf_cls = load_object(self.settings["LOG_FORMATTER"])
        self.logformatter = lf_cls.from_crawler(self)

        self.request_fingerprinter: RequestFingerprinter = create_instance(
            load_object(self.settings["REQUEST_FINGERPRINTER_CLASS"]),
            settings=self.settings,
            crawler=self,
        )

        reactor_class = self.settings["TWISTED_REACTOR"]
        event_loop = self.settings["ASYNCIO_EVENT_LOOP"]
        if init_reactor:
            # this needs to be done after the spider settings are merged,
            # but before something imports twisted.internet.reactor
            if reactor_class:
                install_reactor(reactor_class, event_loop)
            else:
                from twisted.internet import reactor  # noqa: F401
            log_reactor_info()
        if reactor_class:
            verify_installed_reactor(reactor_class)
            if is_asyncio_reactor_installed() and event_loop:
                verify_installed_asyncio_event_loop(event_loop)

        self.extensions = ExtensionManager.from_crawler(self)

        self.settings.freeze()
        self.crawling = False
        self.spider = None
        self.engine: Optional[ExecutionEngine] = None


class CustomCrawlerRunner(CrawlerRunner):
    def create_crawler(self, crawler_or_spidercls):
        if isinstance(crawler_or_spidercls, CustomCrawler):
            return crawler_or_spidercls
        return self._create_crawler(crawler_or_spidercls)

    def _create_crawler(self, spidercls):
        if isinstance(spidercls, six.string_types):
            spidercls = self.spider_loader.load(spidercls)
        return CustomCrawler(spidercls, self.settings)


class CustomCrawlerProcess(CustomCrawlerRunner):
    """
    重写 scrapy.crawler.CrawlerProcess __init__ 方法日志配置处
    其余代码相同（原封不动拷贝）
    """

    def __init__(self, settings=None, install_root_handler=True):
        super().__init__(settings)
        install_shutdown_handlers(self._signal_shutdown)
        # 重写日志配置
        custom_configure_logging(self.settings, install_root_handler)
        log_scrapy_info(self.settings)

    def _signal_shutdown(self, signum, _):
        install_shutdown_handlers(self._signal_kill)
        signame = signal_names[signum]
        logger.info("Received %(signame)s, shutting down gracefully. Send again to force ",
                    {'signame': signame})
        reactor.callFromThread(self._graceful_stop_reactor)

    def _signal_kill(self, signum, _):
        install_shutdown_handlers(signal.SIG_IGN)
        signame = signal_names[signum]
        logger.info('Received %(signame)s twice, forcing unclean shutdown',
                    {'signame': signame})
        reactor.callFromThread(self._stop_reactor)

    def start(self, stop_after_crawl=True):
        """
        This method starts a Twisted `reactor`_, adjusts its pool size to
        :setting:`REACTOR_THREADPOOL_MAXSIZE`, and installs a DNS cache based
        on :setting:`DNSCACHE_ENABLED` and :setting:`DNSCACHE_SIZE`.

        If `stop_after_crawl` is True, the reactor will be stopped after all
        crawlers have finished, using :meth:`join`.

        :param boolean stop_after_crawl: stop or not the reactor when all
            crawlers have finished
        """
        if stop_after_crawl:
            d = self.join()
            # Don't start the reactor if the deferreds are already fired
            if d.called:
                return
            d.addBoth(self._stop_reactor)

        reactor.installResolver(self._get_dns_resolver())
        tp = reactor.getThreadPool()
        tp.adjustPoolsize(maxthreads=self.settings.getint('REACTOR_THREADPOOL_MAXSIZE'))
        reactor.addSystemEventTrigger('before', 'shutdown', self.stop)
        reactor.run(installSignalHandlers=False)  # blocking call

    def _get_dns_resolver(self):
        if self.settings.getbool('DNSCACHE_ENABLED'):
            cache_size = self.settings.getint('DNSCACHE_SIZE')
        else:
            cache_size = 0
        return CachingThreadedResolver(
            reactor=reactor,
            cache_size=cache_size,
            timeout=self.settings.getfloat('DNS_TIMEOUT')
        )

    def _graceful_stop_reactor(self):
        d = self.stop()
        d.addBoth(self._stop_reactor)
        return d

    def _stop_reactor(self, _=None):
        try:
            reactor.stop()
        except RuntimeError:  # raised if already stopped or in shutdown stage
            pass
