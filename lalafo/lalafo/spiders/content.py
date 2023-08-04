import scrapy


class ContentSpider(scrapy.Spider):
    name = "content"
    allowed_domains = ["lalafo.az"]
    start_urls = ["https://lalafo.az/baku/ads/binqdi-qs-3-otaqli-90-kv-m-yeni-tmirli-id-102934449"]

    def parse(self, response):
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
            phone_number = response.css('.phone-item span::text').getall()
            address_description = response.xpath(
                '//div[contains(@class, "description")]/div[contains(@class, "description__wrap")]/p/span/text()').get()
            address = response.xpath(
                '//div[@class="pro-item address"]/div[@class="pro-item__title-wrap"]/p/text()').get()
            region_addres = response.xpath(
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

            yield {
                "link": link,
                "id": id,
                "update_date": update_date,
                "create_date": create_date,
                "price": price,
                "currency": currency,
                "user_name": user_name,
                "user_status": user_status,
                "phone_number": phone_number,
                "address_description": address_description,
                "address": address,
                "region_addres": region_addres,
                "metro_station": metro_station,
                "official_address": official_address,
                "impressions": impressions,
                "view_counts": view_counts,
                "likes": likes,
                "show_button": show_button,
                "short_description": short_description,
                "count_of_rooms": count_of_rooms,
                "area_of_flat": area_of_flat,
                "area_of_property": area_of_property,
                "floor": floor,
                "repair_type": repair_type,
                "flat_type": flat_type,
                "communal_lines": communal_lines
            }
        except Exception as e:
            # Log the exception or handle it as per your requirement.
            # You can also yield an error item if needed.
            self.logger.error(f"An error occurred while parsing: {str(e)}")
            yield {
                "link": link,
                "id": id,
                "update_date": None,
                "create_date": None,
                "price": price,
                "currency": currency,
                "user_name": user_name,
                "user_status": user_status,
                "phone_number": phone_number,
                "address_description": address_description,
                "address": address,
                "region_addres": region_addres,
                "metro_station": metro_station,
                "official_address": official_address,
                "impressions": impressions,
                "view_counts": view_counts,
                "likes": likes,
                "show_button": show_button,
                "short_description": short_description,
                "count_of_rooms": count_of_rooms,
                "area_of_flat": area_of_flat,
                "area_of_property": area_of_property,
                "floor": floor,
                "repair_type": repair_type,
                "flat_type": flat_type,
                "communal_lines": communal_lines
            }
