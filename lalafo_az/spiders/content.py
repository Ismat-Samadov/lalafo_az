import scrapy

from scrapy_playwright.page import PageMethod

class ContentSpider(scrapy.Spider):
    name = "content"
    allowed_domains = ["lalafo.az"]

    # start_urls = [""]
    def start_requests(self):
        yield scrapy.Request(

            url="https://lalafo.az/baku/ads/binqdi-qs-3-otaqli-90-kv-m-yeni-tmirli-id-102934449",
            callback=self.parse,
            meta={
                "playwright": True,
                "playwright_page_methods": [
                    PageMethod("wait_for_selector", '.card-body'),
                ],
            },
        )

    def parse(self, response):
        phone = response.xpath(
            '//*[@id="__next"]/div/div[1]/div/div[3]/div[1]/div[2]/div[2]/div[2]/div/div/div/a/span/text()').getall()
        yield {
            "phone": phone
        }


