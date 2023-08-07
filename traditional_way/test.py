import asyncio
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import pandas as pd
import aiohttp
import nest_asyncio

nest_asyncio.apply()  # Allow running nested event loops in Jupyter Notebook


async def fetch_page(session, url):
    try:
        async with session.get(url) as response:
            return await response.text()
    except Exception as e:
        print(f"Error occurred while fetching {url}: {e}")
        return None

async def extract_phone_numbers(driver):
    phone_numbers = []

    try:
        phone_items = await WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'phone-item')))
        for phone_item in phone_items:
            try:
                phone_number = await phone_item.find_element(By.TAG_NAME, 'span').text.strip()
                phone_numbers.append(phone_number)
            except Exception as e:
                print(f"Error occurred while extracting phone number: {e}")

    except TimeoutException:
        print("Timeout exception occurred while locating 'phone-item' element.")
        pass

    return phone_numbers


async def click_show_buttons(driver, num_buttons):
    try:
        show_buttons = await WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'show-button')))

        for i in range(min(num_buttons, len(show_buttons))):
            if show_buttons[i].is_displayed() and show_buttons[i].is_enabled():
                try:
                    await show_buttons[i].click()
                except Exception as ex:
                    # Handle any exception during click, such as ElementClickInterceptedException
                    print(f"Exception occurred: {ex}")
                await asyncio.sleep(1)  # Add a short delay to allow the content to load (optional)
    except TimeoutException:
        # Handle the TimeoutException if the 'show-button' element is not found
        pass





async def process_link(session, link, driver):
    href = link["href"]
    url = f'https://lalafo.az{href}'
    html_content = await fetch_page(session, url)

    if html_content is not None:
        soup = BeautifulSoup(html_content, "html.parser")

        num_buttons_to_click = 4
        await click_show_buttons(driver, num_buttons_to_click)  # Await click_show_buttons

        extracted_phone_numbers = await extract_phone_numbers(driver)  # Await extract_phone_numbers
        return extracted_phone_numbers
    else:
        return []


async def main_async(all_links):
    # Initialize Chrome WebDriver
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run Chrome WebDriver in headless mode
    driver = webdriver.Chrome(options=chrome_options)

    async with aiohttp.ClientSession() as session:
        tasks = [process_link(session, link, driver) for link in all_links]  # Pass 'driver'
        phone_numbers_list = await asyncio.gather(*tasks)

    # Create a DataFrame and save to CSV
    df = pd.DataFrame(phone_numbers_list, columns=["Phone Numbers"])
    df.to_csv("phone_numbers.csv", index=False)


def main(all_links):
    # Initialize Chrome WebDriver
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run Chrome WebDriver in headless mode
    driver = webdriver.Chrome(options=chrome_options)

    for link in all_links:
        href = link["href"]
        url = f'https://lalafo.az{href}'
        driver.get(url)
        time.sleep(2)

        # Click on the first four "show" buttons
        num_buttons_to_click = 4
        click_show_buttons(driver, num_buttons_to_click)

        extracted_phone_numbers = extract_phone_numbers(driver)
        print(extracted_phone_numbers)

    driver.quit()


if __name__ == "__main__":
    # Get the links using BeautifulSoup
    url = "https://lalafo.az/azerbaijan/nedvizhimost"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    all_links = soup.find_all("a", href=True)

    asyncio.run(main_async(all_links))
    main(all_links)
