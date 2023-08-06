# import scrapy
# from scrapy.item import Item, Field
# from typing import Iterable, Union
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
#
#
# class PropertyItem(Item):
#     Page = Field()
#     URL = Field()
#     id = Field()
#     update_date = Field()
#     create_date = Field()
#     price = Field()
#     currency = Field()
#     user_name = Field()
#     user_status = Field()
#     phone_number = Field()
#     address_description = Field()
#     address = Field()
#     region_address = Field()
#     metro_station = Field()
#     official_address = Field()
#     impressions = Field()
#     view_counts = Field()
#     likes = Field()
#     show_button = Field()
#     short_description = Field()
#     count_of_rooms = Field()
#     area_of_flat = Field()
#     area_of_property = Field()
#     floor = Field()
#     repair_type = Field()
#     flat_type = Field()
#     communal_lines = Field()
#
#
# class LalafoContentSpider(scrapy.Spider):
#     name = 'clicks'
#     start_urls = ['https://lalafo.az/azerbaijan/nedvizhimost']
#
#     def parse(self, response) -> Iterable[Union[scrapy.Request, PropertyItem]]:
#         # Extract the hrefs from the current page
#         hrefs = response.css('a::attr(href)').extract()
#
#         # Filter and clean the hrefs to keep only property URLs
#         property_hrefs = [href for href in hrefs if '/ads/' in href]
#
#         # Yield each property URL with the page number
#         page_number = int(response.url.split('=')[-1]) if 'page=' in response.url else 1
#         for href in property_hrefs:
#             yield PropertyItem({
#                 'Page': page_number,
#                 'URL': response.urljoin(href)
#             })
#
#             # Now, yield a request for each property URL to parse its content
#             yield scrapy.Request(response.urljoin(href), callback=self.parse_content)
#
#         # Find and follow the "Next" button
#         next_page = response.css('a.paginator-item.arrow.right::attr(href)').get()
#         if next_page:
#             yield scrapy.Request(response.urljoin(next_page), callback=self.parse)
#
#     def parse_content(self, response):
#         try:
#             id = response.xpath(
#                 '//div[@class="about-ad-info__id"]/span[contains(@style, "color:#737d9b")]/text()').get()
#             link = response.xpath('/html/head/link[6]/@href').get()
#             update_date = response.xpath(
#                 '//div[@class="about-ad-info__date"]/span[contains(text(), "Yenilənmə tarixi")]/following-sibling::span/text()').get()
#             create_date = response.xpath(
#                 '//div[@class="about-ad-info__date"]/span[contains(text(), "Yaradılma vaxtı")]/following-sibling::span/text()').get()
#             price = response.xpath('//span[@class="price"]/text()').get()
#             currency = response.xpath('//span[@class="currency"]/text()').get()
#             user_name = response.xpath('//span[@class="userName-text"]/text()').get()
#             user_status = response.xpath('//p[@class="LFParagraph size-14 userStatus"]/text()').get()
#
#             # Initialize the Chrome webdriver
#             options = webdriver.ChromeOptions()
#             options.add_argument('--headless')  # Run in headless mode so that the browser is not displayed
#             driver = webdriver.Chrome(options=options)
#
#             # Open the property URL using Selenium to interact with the page
#             driver.get(response.url)
#
#             # Find and click the "Show Phone Number" button
#             show_button = WebDriverWait(driver, 10).until(
#                 EC.presence_of_element_located((By.XPATH, '//button[@class="show-button"]'))
#             )
#             show_button.click()
#
#             # Wait for the phone number to be loaded
#             phone_number_element = WebDriverWait(driver, 10).until(
#                 EC.presence_of_element_located((By.CSS_SELECTOR, '.phone-item span'))
#             )
#
#             # Scrape the phone number
#             phone_number = phone_number_element.text
#
#             # Close the driver as we have obtained the phone number
#             driver.quit()
#
#             address_description = response.xpath(
#                 '//div[contains(@class, "description")]/div[contains(@class, "description__wrap")]/p/span/text()').get()
#             address = response.xpath(
#                 '//div[@class="pro-item address"]/div[@class="pro-item__title-wrap"]/p/text()').get()
#             region_address = response.xpath(
#                 '//li/p[@class="Paragraph secondary  " and contains(text(), "Rayon:")]/following-sibling::a[@class="LinkText primary-black  extra-small "]/text()').get()
#             metro_station = response.xpath(
#                 '//li/p[@class="Paragraph secondary  " and contains(text(), "Metro stansiyası:")]/following-sibling::a[@class="LinkText primary-black  extra-small "]/text()').get()
#             official_address = response.xpath(
#                 '//li/p[@class="Paragraph secondary  " and contains(text(), "İnzibati rayonlar:")]/following-sibling::a[@class="LinkText primary-black  extra-small "]/text()').get()
#             impressions = response.xpath(
#                 '//span[@class="Caption primary " and contains(text(), "Göstərilmə")]/text()').get()
#             view_counts = response.xpath(
#                 '//div[@class="details-page__statistic-bar css-q8sniu"]//ul/li[1]/span[@class="Caption primary "]/text()').get()
#             likes = response.xpath(
#                 '//div[@class="details-page__statistic-bar css-q8sniu"]//ul/li[2]/span[@class="Caption primary "]/text()').get()
#             show_button = response.xpath('//button[@class="show-button"]').get()
#             short_description = response.xpath('//h1[@class="Heading secondary-small " ]/text()').get()
#             count_of_rooms = response.xpath(
#                 '//li/p[@class="Paragraph secondary  " and contains(text(), "Otaqların sayı:")]/following-sibling::a[@class="LinkText primary-black  extra-small "]/text()').get()
#             area_of_flat = response.xpath(
#                 '//li/p[@class="Paragraph secondary  " and contains(text(), "Sahə (m2):")]/following-sibling::p[@class="Paragraph secondary  "]/text()').get()
#             area_of_property = response.xpath(
#                 '//li/p[@class="Paragraph secondary  " and contains(text(), "Torpaq sahəsi (Sot):")]/following-sibling::p[@class="Paragraph secondary  "]/text()').get()
#             floor = response.xpath(
#                 '//li/p[@class="Paragraph secondary  " and contains(text(), "Mərtəbələrin sayı:")]/following-sibling::p[@class="Paragraph secondary  "]/text()').get()
#             repair_type = response.xpath(
#                 "//ul[@class='details-page__params css-tl517w']/li[8]/a/text()").get()
#             flat_type = response.xpath(
#                 '//ul[@class="details-page__params css-tl517w"]/li[p[contains(., "Evin şəraiti:")]]/a[@class="LinkText primary-black  extra-small "]/text()').getall()
#             communal_lines = response.xpath("//ul[@class='details-page__params css-tl517w']/li[9]/a/text()").getall()
#
#             # Yield the data for the property along with the page number and URL
#             yield PropertyItem({
#                 'Page': int(response.url.split('=')[-1]) if 'page=' in response.url else 1,
#                 'URL': response.url,
#                 'id': id,
#                 'update_date': update_date,
#                 'create_date': create_date,
#                 'price': price,
#                 'currency': currency,
#                 'user_name': user_name,
#                 'user_status': user_status,
#                 'phone_number': phone_number,
#                 'address_description': address_description,
#                 'address': address,
#                 'region_address': region_address,
#                 'metro_station': metro_station,
#                 'official_address': official_address,
#                 'impressions': impressions,
#                 'view_counts': view_counts,
#                 'likes': likes,
#                 'show_button': show_button,
#                 'short_description': short_description,
#                 'count_of_rooms': count_of_rooms,
#                 'area_of_flat': area_of_flat,
#                 'area_of_property': area_of_property,
#                 'floor': floor,
#                 'repair_type': repair_type,
#                 'flat_type': flat_type,
#                 'communal_lines': communal_lines
#             })
#         except Exception as e:
#             # Log the exception or handle it as per your requirement.
#             # You can also yield an error item if needed.
#             self.logger.error(f"An error occurred while parsing: {str(e)}")
#             yield PropertyItem({
#                 'Page': int(response.url.split('=')[-1]) if 'page=' in response.url else 1,
#                 'URL': response.url,
#                 'id': None,
#                 'update_date': None,
#                 'create_date': None,
#                 'price': None,
#                 'currency': None,
#                 'user_name': None,
#                 'user_status': None,
#                 'phone_number': None,
#                 'address_description': None,
#                 'address': None,
#                 'region_address': None,
#                 'metro_station': None,
#                 'official_address': None,
#                 'impressions': None,
#                 'view_counts': None,
#                 'likes': None,
#                 'show_button': None,
#                 'short_description': None,
#                 'count_of_rooms': None,
#                 'area_of_flat': None,
#                 'area_of_property': None,
#                 'floor': None,
#                 'repair_type': None,
#                 'flat_type': None,
#                 'communal_lines': None
#             })

import scrapy
from scrapy.item import Item, Field
from typing import Iterable, Union


class PropertyItem(Item):
    Page = Field()
    URL = Field()
    id = Field()
    update_date = Field()
    create_date = Field()
    price = Field()
    currency = Field()
    user_name = Field()
    user_status = Field()
    phone_number = Field()
    address_description = Field()
    address = Field()
    region_address = Field()
    metro_station = Field()
    official_address = Field()
    impressions = Field()
    view_counts = Field()
    likes = Field()
    show_button = Field()
    short_description = Field()
    count_of_rooms = Field()
    area_of_flat = Field()
    area_of_property = Field()
    floor = Field()
    repair_type = Field()
    flat_type = Field()
    communal_lines = Field()


class LalafoContentSpider(scrapy.Spider):
    name = 'clicks'
    start_urls = ['https://lalafo.az/azerbaijan/nedvizhimost']

    def parse(self, response) -> Iterable[Union[scrapy.Request, PropertyItem]]:
        # Extract the hrefs from the current page
        hrefs = response.css('a::attr(href)').extract()

        # Filter and clean the hrefs to keep only property URLs
        property_hrefs = [href for href in hrefs if '/ads/' in href]

        # Yield each property URL with the page number
        page_number = int(response.url.split('=')[-1]) if 'page=' in response.url else 1
        for href in property_hrefs:
            yield PropertyItem({
                'Page': page_number,
                'URL': response.urljoin(href)
            })

            # Now, yield a request for each property URL to parse its content
            yield scrapy.Request(response.urljoin(href), callback=self.parse_content)

        # Find and follow the "Next" button
        next_page = response.css('a.paginator-item.arrow.right::attr(href)').get()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def parse_content(self, response):
        try:
            id = response.xpath(
                '//div[@class="about-ad-info__id"]/span[contains(@style, "color:#737d9b")]/text()').get()
            link = response.xpath('/html/head/link[6]/@href').get()
            update_date = response.xpath(
                '//div[@class="about-ad-info__date"]/span[contains(text(), "Yenilənmə tarixi")]/following-sibling::span/text()').get()
            create_date = response.xpath(
                '//div[@class="about-ad-info__date"]/span[contains(text(), "Yaradılma vaxtı")]/following-sibling::span/text()').get()
            price = response.xpath('//span[@class="price"]/text()').get()
            currency = response.xpath('//span[@class="currency"]/text()').get()
            user_name = response.xpath('//span[@class="userName-text"]/text()').get()
            user_status = response.xpath('//p[@class="LFParagraph size-14 userStatus"]/text()').get()

            # Get the phone number (without using Selenium)
            phone_number = self.get_phone_number(response)

            address_description = response.xpath(
                '//div[contains(@class, "description")]/div[contains(@class, "description__wrap")]/p/span/text()').get()
            address = response.xpath(
                '//div[@class="pro-item address"]/div[@class="pro-item__title-wrap"]/p/text()').get()
            region_address = response.xpath(
                '//li/p[@class="Paragraph secondary  " and contains(text(), "Rayon:")]/following-sibling::a[@class="LinkText primary-black  extra-small "]/text()').get()
            metro_station = response.xpath(
                '//li/p[@class="Paragraph secondary  " and contains(text(), "Metro stansiyası:")]/following-sibling::a[@class="LinkText primary-black  extra-small "]/text()').get()
            official_address = response.xpath(
                '//li/p[@class="Paragraph secondary  " and contains(text(), "İnzibati rayonlar:")]/following-sibling::a[@class="LinkText primary-black  extra-small "]/text()').get()
            impressions = response.xpath(
                '//span[@class="Caption primary " and contains(text(), "Göstərilmə")]/text()').get()
            view_counts = response.xpath(
                '//div[@class="details-page__statistic-bar css-q8sniu"]//ul/li[1]/span[@class="Caption primary "]/text()').get()
            likes = response.xpath(
                '//div[@class="details-page__statistic-bar css-q8sniu"]//ul/li[2]/span[@class="Caption primary "]/text()').get()
            show_button = response.xpath('//button[@class="show-button"]').get()
            short_description = response.xpath('//h1[@class="Heading secondary-small " ]/text()').get()
            count_of_rooms = response.xpath(
                '//li/p[@class="Paragraph secondary  " and contains(text(), "Otaqların sayı:")]/following-sibling::a[@class="LinkText primary-black  extra-small "]/text()').get()
            area_of_flat = response.xpath(
                '//li/p[@class="Paragraph secondary  " and contains(text(), "Sahə (m2):")]/following-sibling::p[@class="Paragraph secondary  "]/text()').get()
            area_of_property = response.xpath(
                '//li/p[@class="Paragraph secondary  " and contains(text(), "Torpaq sahəsi (Sot):")]/following-sibling::p[@class="Paragraph secondary  "]/text()').get()
            floor = response.xpath(
                '//li/p[@class="Paragraph secondary  " and contains(text(), "Mərtəbələrin sayı:")]/following-sibling::p[@class="Paragraph secondary  "]/text()').get()
            repair_type = response.xpath(
                "//ul[@class='details-page__params css-tl517w']/li[8]/a/text()").get()
            flat_type = response.xpath(
                '//ul[@class="details-page__params css-tl517w"]/li[p[contains(., "Evin şəraiti:")]]/a[@class="LinkText primary-black  extra-small "]/text()').getall()
            communal_lines = response.xpath("//ul[@class='details-page__params css-tl517w']/li[9]/a/text()").getall()

            # Yield the data for the property along with the page number and URL
            yield PropertyItem({
                'Page': int(response.url.split('=')[-1]) if 'page=' in response.url else 1,
                'URL': response.url,
                'id': id,
                'update_date': update_date,
                'create_date': create_date,
                'price': price,
                'currency': currency,
                'user_name': user_name,
                'user_status': user_status,
                'phone_number': phone_number,
                'address_description': address_description,
                'address': address,
                'region_address': region_address,
                'metro_station': metro_station,
                'official_address': official_address,
                'impressions': impressions,
                'view_counts': view_counts,
                'likes': likes,
                'show_button': show_button,
                'short_description': short_description,
                'count_of_rooms': count_of_rooms,
                'area_of_flat': area_of_flat,
                'area_of_property': area_of_property,
                'floor': floor,
                'repair_type': repair_type,
                'flat_type': flat_type,
                'communal_lines': communal_lines
            })
        except Exception as e:
            # Log the exception or handle it as per your requirement.
            # You can also yield an error item if needed.
            self.logger.error(f"An error occurred while parsing: {str(e)}")
            yield PropertyItem({
                'Page': int(response.url.split('=')[-1]) if 'page=' in response.url else 1,
                'URL': response.url,
                'id': None,
                'update_date': None,
                'create_date': None,
                'price': None,
                'currency': None,
                'user_name': None,
                'user_status': None,
                'phone_number': None,
                'address_description': None,
                'address': None,
                'region_address': None,
                'metro_station': None,
                'official_address': None,
                'impressions': None,
                'view_counts': None,
                'likes': None,
                'show_button': None,
                'short_description': None,
                'count_of_rooms': None,
                'area_of_flat': None,
                'area_of_property': None,
                'floor': None,
                'repair_type': None,
                'flat_type': None,
                'communal_lines': None
            })

    def get_phone_number(self, response):
        # Extract the phone number from the page directly (without using Selenium)
        phone_number = response.css('.phone-item span::text').get()
        return phone_number
