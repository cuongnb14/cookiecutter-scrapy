import random
from urllib.parse import urlparse

import requests
from scrapy import signals
from scrapy.exceptions import CloseSpider

from {{cookiecutter.project_slug}}.configs import settings


class BaseProxyMiddleware(object):
    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def _get_proxies(self):
        """
        This method must return list of proxies with format: <scheme>://<username>:<password>@<ip>:<port>
        """
        raise NotImplementedError()

    def spider_opened(self, spider):
        if spider.name not in []:
            spider.proxies = self._get_proxies()
            if not spider.proxies:
                raise Exception("Error: Can't found any proxies")
            spider.logger.info('Use %s proxies for spider %s: %s', len(spider.proxies), spider.name, spider.proxies)

    def process_request(self, request, spider):
        if spider.name not in []:
            parsed_uri = urlparse(request.url)
            if spider.proxies:
                if parsed_uri.netloc not in settings.PROXY_IGNORE_HOST:
                    proxies = spider.proxies
                    proxy = random.choice(proxies)
                    request.meta['proxy'] = proxy
                    request.meta['raw_proxy'] = proxy  # Because request.meta['proxy'] is removed auth in url
            else:
                raise CloseSpider("No proxy to use")


    def process_response(self, request, response, spider):
        if response.status == 429:
            spider.logger.info('removing {}'.format(request.meta['proxy']))
            if request.meta['raw_proxy'] in spider.proxies:
                spider.proxies.remove(request.meta['raw_proxy'])
                spider.logger.info('removed {}'.format(request.meta['proxy']))
            if not spider.proxies:
                raise CloseSpider("No proxy to use")

        return response
