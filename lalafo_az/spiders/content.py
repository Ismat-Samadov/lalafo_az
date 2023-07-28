import scrapy
from scrapy_splash import SplashRequest


class ContentSpider(scrapy.Spider):
    name = "content"
    allowed_domains = ["lalafo.az"]
    start_urls = ["https://lalafo.az/baku/ads/binqdi-qs-3-otaqli-90-kv-m-yeni-tmirli-id-102934449"]

    script = '''
             function main(splash, args)
                local success, error_message
                success, error_message = pcall(function()
                    splash.private_mode_enabled = false
                    url = args.url
                    assert(splash:go(url))
                    splash:set_viewport_full()
                end)
                if not success then
                    splash:log("Error: " .. error_message)
                end

                return {
                    html = splash:html()
                }
            end
            '''

    def start_requests(self):
        yield SplashRequest(url='https://lalafo.az/baku/ads/binqdi-qs-3-otaqli-90-kv-m-yeni-tmirli-id-102934449',
                            callback=self.parse,
                            endpoint='execute',
                            args={'lua_source': self.script}
                            )

    def parse_car_details(self, response):
        href = response.request.meta['href']

        # Define default values in case XPath selectors don't match any elements
        default_value = None

        try:
            phone = response.xpath(
                '//*[@id="__next"]/div/div[1]/div/div[3]/div[1]/div[2]/div[2]/div[2]/div/div/div/a/span/text()').getall()
            yield {
                "phone": phone
            }

        except Exception as e:
            # Log the error and yield an item with default values
            self.logger.error(f"Error parsing details for URL: {response.url}. Error: {repr(e)}")
            yield {
                'phone': default_value
            }
