import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class ButtonClickSpider(scrapy.Spider):
    name = 'succes'
    start_urls = ['https://lalafo.az/baku/ads/baki-hovsan-qs-74-kv-m-3-otaqli-hovuzsuz-kombi-qaz-isiq-id-92773245']

    def __init__(self):
        # Initialize the Selenium webdriver
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Run Chrome in headless mode (without GUI)
        self.driver = webdriver.Chrome(options=options)

    def parse(self, response):
        self.driver.get(response.url)
        time.sleep(2)

        # Click on the first four "show" buttons
        num_buttons_to_click = 4
        self.click_show_buttons(num_buttons_to_click)

        # Extract phone numbers
        phone_numbers = self.extract_phone_numbers()
        yield {'phone_numbers': phone_numbers}

        self.driver.quit()

    def click_show_buttons(self, num_buttons):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'show-button')))
        show_buttons = self.driver.find_elements(By.CLASS_NAME, 'show-button')

        for i in range(min(num_buttons, len(show_buttons))):
            show_buttons[i].click()
            time.sleep(1)  # Add a short delay to allow the content to load (optional)

    def extract_phone_numbers(self):
        phone_numbers = []

        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'phone-item')))
        phone_items = self.driver.find_elements(By.CLASS_NAME, 'phone-item')

        for phone_item in phone_items:
            phone_number = phone_item.find_element(By.TAG_NAME, 'span').text.strip()
            phone_numbers.append(phone_number)

        return phone_numbers
