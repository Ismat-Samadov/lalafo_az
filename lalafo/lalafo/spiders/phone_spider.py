import scrapy
from scrapy_splash import SplashRequest

class PhoneSpider(scrapy.Spider):
    name = 'phone_spider'
    start_urls = ['https://lalafo.az/baku/ads/baki-hovsan-qs-74-kv-m-3-otaqli-hovuzsuz-kombi-qaz-isiq-id-92773245']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parse, args={'wait': 2})

    def parse(self, response):
        # Click the "Show" button using JavaScript
        script = """
        function main(splash)
            splash:wait(0.5)
            local button = splash:select('button.show-button')
            button:mouse_click()
            splash:wait(2)
            return splash:html()
        end
        """

        yield SplashRequest(url=response.url, callback=self.parse_after_click,
                            endpoint='execute', args={'lua_source': script, 'wait': 2})

    def parse_after_click(self, response):
        # Extract the revealed phone numbers from the updated response
        phone_numbers = response.css('div.phone-wrap a::attr(href)').getall()

        yield {
            'phone_numbers': phone_numbers
        }
