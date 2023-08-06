# import scrapy
# from typing import Iterable, Union
#
#
# class LalafoContentSpider(scrapy.Spider):
#     name = 'lalafo_content'
#     start_urls = ['https://lalafo.az/azerbaijan/nedvizhimost']
#
#     def parse(self, response) -> Iterable[Union[scrapy.Request, scrapy.Item]]:
#         # Extract the hrefs from the current page
#         hrefs = response.css('a::attr(href)').extract()
#
#         # Filter and clean the hrefs to keep only property URLs
#         property_hrefs = [href for href in hrefs if '/ads/' in href]
#
#         # Yield each property URL with the page number
#         page_number = int(response.url.split('=')[-1]) if 'page=' in response.url else 1
#         for href in property_hrefs:
#             yield {
#                 'Page': page_number,
#                 'URL': response.urljoin(href)
#             }
#             # Now, yield a request for each property URL to parse its content
#             yield scrapy.Request(response.urljoin(href), callback=self.parse_content)
#
#             # Find and follow the "Next" button
#         next_page = response.css('a.paginator-item.arrow.right::attr(href)').get()
#         if next_page:
#             yield scrapy.Request(response.urljoin(next_page), callback=self.parse)
#
#     def parse_content(self, response):
#
