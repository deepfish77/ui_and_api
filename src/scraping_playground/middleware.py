from scrapy.exceptions import NotConfigured


class ProxyMiddleware(object):

    def __init__(self, settings):
        if not settings.getbool("HTTPPROXY_ENABLED"):
            raise NotConfigured

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_request(self, request, spider):
        proxy = request.meta.get("proxy")
        if proxy:
            request.meta["proxy"] = proxy
