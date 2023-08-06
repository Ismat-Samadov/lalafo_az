import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class LalafoSpider(scrapy.Spider):
    name = 'test2'
    start_urls = ['https://lalafo.az/baku/ads/baki-hovsan-qs-74-kv-m-3-otaqli-hovuzsuz-kombi-qaz-isiq-id-92773245']

    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=self.chrome_options)

    def parse(self, response):
        self.driver.get(response.url)
        time.sleep(2)

        # Click on the fourth "show" button
        button_index_to_click = 3
        self.click_show_button(button_index_to_click)

        # Extract phone numbers after clicking the button
        extracted_phone_numbers = self.extract_phone_numbers()
        for phone_number in extracted_phone_numbers:
            yield {'phone_number': phone_number}

        self.driver.quit()

    def click_show_button(self, button_index):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'show-button')))
        show_buttons = self.driver.find_elements(By.CLASS_NAME, 'show-button')

        if 0 <= button_index < len(show_buttons):
            show_buttons[button_index].click()
            time.sleep(1)

    def extract_phone_numbers(self):
        phone_numbers = []

        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'phone-item')))
        phone_items = self.driver.find_elements(By.CLASS_NAME, 'phone-item')

        for phone_item in phone_items:
            phone_number = phone_item.find_element(By.TAG_NAME, 'span').text.strip()
            phone_numbers.append(phone_number)

        return phone_numbers
