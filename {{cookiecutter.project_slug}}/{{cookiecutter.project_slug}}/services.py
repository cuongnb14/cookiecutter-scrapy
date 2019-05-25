import requests
from lxml import html
from etsycrawl import settings
from multiprocessing.pool import ThreadPool

from .discord import discord

def get_free_proxies():
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


def check_proxy(proxy):
    try:
        requests.get("https://example.org", proxies={'https': proxy}, timeout=3)
        return proxy
    except Exception as e:
        return None


def get_proxies():
    """
    Get list proxies from cms

    :return: list
    """
    # headers = {
    #     'token': settings.INTERNAL_TOKEN
    # }
    # response = requests.get(settings.GET_PROXY_API, headers=headers)
    # proxies = [x['url'] for x in response.json()["results"]]
    proxies = get_free_proxies()

    proxies = get_free_proxies()

    pool = ThreadPool(50)
    active_proxies = pool.map(check_proxy, proxies)
    active_proxies = [x for x in active_proxies if x is not None]

    if not active_proxies:
        discord.send_message("No proxy to use")
        raise Exception("No proxy to use")

    return active_proxies
