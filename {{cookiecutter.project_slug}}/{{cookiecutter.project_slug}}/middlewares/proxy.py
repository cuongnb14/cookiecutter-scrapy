from {{cookiecutter.project_slug}}.middlewares.base_proxy import BaseProxyMiddleware


class ProxyMiddleware(BaseProxyMiddleware):

    def _get_proxies(self):
        with open("proxies.txt", 'r') as data:
            lines = data.readlines()
            proxies = []
            for line in lines:
                line = line.strip()
                if line:
                    proxies.append(line)
            return proxies