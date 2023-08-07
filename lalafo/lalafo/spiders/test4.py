import scrapy
from scrapy.item import Item, Field
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import asyncio
import aiohttp
from bs4 import BeautifulSoup


class PhoneItem(Item):
    url = Field()
    phone_numbers = Field()


class CombinedSpider(CrawlSpider):
    name = 'test4'
    allowed_domains = ['lalafo.az']
    start_urls = ['https://lalafo.az/azerbaijan/nedvizhimost']

    rules = (
        Rule(LinkExtractor(allow=(), deny=('/azerbaijan/nedvizhimost',)), callback='parse_item', follow=True,
             errback='handle_error'),
    )

    def __init__(self):
        super(CombinedSpider, self).__init__()
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=options)
        self.semaphore = asyncio.Semaphore(5)  # Limit concurrent requests to 5

    async def fetch(self, session, url):
        async with self.semaphore:
            async with session.get(url) as response:
                return await response.text()

    async def parse_item(self, response):
        self.driver.get(response.url)
        time.sleep(2)

        # Click on the first four "show" buttons
        num_buttons_to_click = 4
        self.click_show_buttons(num_buttons_to_click)

        # Extract phone numbers asynchronously
        phone_numbers = await self.extract_phone_numbers_async()

        # Load the item with data
        loader = ItemLoader(item=PhoneItem(), response=response)
        loader.add_value('url', response.url)
        loader.add_value('phone_numbers', phone_numbers)
        yield loader.load_item()

    def click_show_buttons(self, num_buttons):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'show-button')))
        show_buttons = self.driver.find_elements(By.CLASS_NAME, 'show-button')

        for i in range(min(num_buttons, len(show_buttons))):
            show_buttons[i].click()
            time.sleep(1)  # Add a short delay to allow the content to load (optional)

    async def extract_phone_numbers_async(self):
        phone_numbers = []

        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'phone-item')))
        phone_items = self.driver.find_elements(By.CLASS_NAME, 'phone-item')

        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch(session, phone_item.get_attribute('href')) for phone_item in phone_items]
            phone_number_responses = await asyncio.gather(*tasks)

        for response_text in phone_number_responses:
            soup = BeautifulSoup(response_text, 'html.parser')
            phone_number = soup.select_one('.phone-item span')
            if phone_number:
                phone_numbers.append(phone_number.text.strip())
            else:
                phone_numbers.append("PHONE_NUMBER_NOT_FOUND")

        return phone_numbers

    def handle_error(self, failure):
        # Log the error or perform any necessary action when an error occurs
        pass

    def closed(self, reason):
        self.driver.quit()
