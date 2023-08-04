import scrapy
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from scrapy_splash import SplashRequest


class LinkSpider(CrawlSpider):
    name = "link"

    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        splash_args = {'wait': 3}
        for url in self.settings.get('START_URLS', []):
            yield SplashRequest(url,
                                callback=self.parse,
                                args=splash_args,
                                headers=headers
                                )

    def parse(self, response):
        hrefs = response.xpath(
            '//div[@class="AdTileHorizontalMainInfo"]//a[@class="AdTileHorizontalTitle business"]/@href').getall()
        for href in hrefs:
            yield {
                "href": href
            }
