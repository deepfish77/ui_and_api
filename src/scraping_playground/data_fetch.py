import scrapy
from scrapy import signals
from scrapy.exceptions import CloseSpider

PROXY_LIST = [
    "proxy1.com:8080",
    "proxy2.com:8080",
    "proxy3.com:8080",
]
ALLOWED_DOMAINS = ["example.com"]

START_URLS = [
    "http://www.example.com/",
]


class ExampleSpider(scrapy.Spider):
    name = "example"
    allowed_domains = ALLOWED_DOMAINS
    start_urls = START_URLS

    def __init__(self, *args, **kwargs):
        super(ExampleSpider, self).__init__(*args, **kwargs)
        self.proxy_list = PROXY_LIST
        self.proxy_index = 0

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                meta={"proxy": self.get_next_proxy()},
                dont_filter=True,
                callback=self.parse,
            )

    def get_next_proxy(self):
        proxy = self.proxy_list[self.proxy_index]
        self.proxy_index = (self.proxy_index + 1) % len(self.proxy_list)
        return f"http://{proxy}"

    def parse(self, response):
        # Example parsing logic
        title = response.css("title::text").get()
        yield {"title": title, "proxy_used": response.meta.get("proxy")}

        # Follow links if needed
        for href in response.css("a::attr(href)").getall():
            yield response.follow(
                href, self.parse, meta={"proxy": self.get_next_proxy()}
            )
