import scrapy


class BossSpiderSpider(scrapy.Spider):
    name = "boss_spider"
    allowed_domains = ["'zhipin.com'"]
    start_urls = ["https://'zhipin.com'"]

    def parse(self, response):
        pass
