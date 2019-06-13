from scrapy import signals
import requests
from lxml import html
from multiprocessing.pool import ThreadPool
import random
from urllib.parse import urlparse
from azura_crawler.configs import settings


class FreeProxyMiddleware(object):
    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)

        return s

    def _get_free_proxies(self):
        page = requests.get('https://free-proxy-list.net/')
        tree = html.fromstring(page.content)

        rows = tree.xpath("//tr")

        proxies = []
        for row in rows:
            try:
                ip = row.xpath("td/text()")[0]
                port = row.xpath("td/text()")[1]
                proxies.append("http://{}:{}".format(ip, port))
            except Exception:
                pass
        return proxies

    def _check_proxy(self, proxy):
        try:
            requests.get("https://example.org", proxies={'https': proxy}, timeout=3)
            return proxy
        except Exception as e:
            return None

    def _get_active_proxies(self, max_proxy=20):
        proxies = self._get_free_proxies()

        pool = ThreadPool(50)
        active_proxies = pool.map(self._check_proxy, proxies)
        active_proxies = [x for x in active_proxies if x is not None]

        if not active_proxies:
            discord.send_message("No proxy to use")
            raise Exception("No proxy to use")

        return active_proxies[:max_proxy]


    def spider_opened(self, spider):
        if spider.name not in ["image", "image_raw_product"]:
            spider.logger.info('Get list proxies from CMS ...')
            spider.proxies = self._get_active_proxies()
            spider.logger.info('{} proxies for spider {}: {}'.format(len(spider.proxies), spider.name, spider.proxies))

    def process_request(self, request, spider):
        if spider.name not in ["image", "image_raw_product"]:
            parsed_uri = urlparse(request.url)
            if spider.proxies:
                if parsed_uri.netloc not in settings.PROXY_IGNORE_HOST:
                    proxies = spider.proxies
                    proxy = random.choice(proxies)
                    request.meta['proxy'] = proxy