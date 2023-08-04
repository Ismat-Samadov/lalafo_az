import scrapy
from scrapy_splash import SplashRequest


class ContentSpider(scrapy.Spider):
    name = "click"
    allowed_domains = ["lalafo.az"]
    start_urls = ["https://lalafo.az/baku/ads/binqdi-qs-3-otaqli-90-kv-m-yeni-tmirli-id-102934449"]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 3})

    def parse(self, response):
        # Extracting the "show" button element
        show_button = response.xpath('//button[@class="show-button"]')
        if show_button:
            # Clicking the "show" button using Splash
            yield SplashRequest(url=response.url, callback=self.after_show_button_click,
                                args={'wait': 3, 'lua_source': self.lua_script})
        else:
            # If "show" button is not present, yield the results directly
            yield self.process_item(response)

    def after_show_button_click(self, response):
        # After clicking the "show" button, call the process_item function to extract data
        yield self.process_item(response)

    def process_item(self, response):
        yield {
            "link": response.url,
            "id": response.xpath(
                '//div[@class="about-ad-info__id"]/span[contains(@style, "color:#737d9b")]/text()').get(),
            "update_date": response.xpath(
                '//div[@class="about-ad-info__date"]/span[contains(text(), "Yenilənmə tarixi")]/following-sibling::span/text()').get(),
            "create_date": response.xpath(
                '//div[@class="about-ad-info__date"]/span[contains(text(), "Yaradılma vaxtı")]/following-sibling::span/text()').get(),
            "price": response.xpath('//span[@class="price"]/text()').get(),
            "currency": response.xpath('//span[@class="currency"]/text()').get(),
            "user_name": response.xpath('//span[@class="userName-text"]/text()').get(),
            "user_status": response.xpath('//p[@class="LFParagraph size-14 userStatus"]/text()').get(),
            "phone_number": response.css(
                'div.phone-number__wrap span::text').getall(),
            "address_description": response.xpath(
                '//div[contains(@class, "description")]/div[contains(@class, "description__wrap")]/p/span/text()').get(),
            "address": response.xpath(
                '//div[@class="pro-item address"]/div[@class="pro-item__title-wrap"]/p/text()').get(),
            "region_addres": response.xpath(
                '//li/p[@class="Paragraph secondary  " and contains(text(), "Rayon:")]/following-sibling::a[@class="LinkText primary-black  extra-small "]/text()').get(),
            "metro_station": response.xpath(
                '//li/p[@class="Paragraph secondary  " and contains(text(), "Metro stansiyası:")]/following-sibling::a[@class="LinkText primary-black  extra-small "]/text()').get(),
            "official_address": response.xpath(
                '//li/p[@class="Paragraph secondary  " and contains(text(), "İnzibati rayonlar:")]/following-sibling::a[@class="LinkText primary-black  extra-small "]/text()').get(),
            "impressions": response.xpath(
                '//span[@class="Caption primary " and contains(text(), "Göstərilmə")]/text()').get(),
            "view_counts": response.xpath(
                '//div[@class="details-page__statistic-bar css-q8sniu"]//ul/li[1]/span[@class="Caption primary "]/text()').get(),
            "likes": response.xpath(
                '//div[@class="details-page__statistic-bar css-q8sniu"]//ul/li[2]/span[@class="Caption primary "]/text()').get(),
            "short_description": response.xpath('//h1[@class="Heading secondary-small "]/text()').get(),
            "count_of_rooms": response.xpath(
                '//li/p[@class="Paragraph secondary  " and contains(text(), "Otaqların sayı:")]/following-sibling::a[@class="LinkText primary-black  extra-small "]/text()').get(),
            "area_of_flat": response.xpath(
                '//li/p[@class="Paragraph secondary  " and contains(text(), "Sahə (m2):")]/following-sibling::p[@class="Paragraph secondary  "]/text()').get(),
            "area_of_property": response.xpath(
                '//li/p[@class="Paragraph secondary  " and contains(text(), "Torpaq sahəsi (Sot):")]/following-sibling::p[@class="Paragraph secondary  "]/text()').get(),
            "floor": response.xpath(
                '//li/p[@class="Paragraph secondary  " and contains(text(), "Mərtəbələrin sayı:")]/following-sibling::p[@class="Paragraph secondary  "]/text()').get(),
            "repair_type": response.xpath("//ul[@class='details-page__params css-tl517w']/li[8]/a/text()").get(),
            "flat_type": response.xpath(
                '//ul[@class="details-page__params css-tl517w"]/li[p[contains(., "Evin şəraiti:")]]/a[@class="LinkText primary-black  extra-small "]/text()').getall(),
            "communal_lines": response.xpath(
                "//ul[@class='details-page__params css-tl517w']/li[9]/a/text()").getall()
        }

    # Lua script to click the "show" button
    lua_script = """
    function main(splash)
        splash:wait(3)
        local show_button = splash:select('button.show-button')
        if show_button then
            show_button:mouse_click()
            splash:wait(3)
        end
        return splash:html()
    end
    """
