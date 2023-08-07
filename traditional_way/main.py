import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def click_show_buttons(driver, num_buttons):
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'show-button')))
        show_buttons = driver.find_elements(By.CLASS_NAME, 'show-button')
        for i in range(min(num_buttons, len(show_buttons))):
            show_buttons[i].click()
            time.sleep(2)
    except TimeoutError:
        print("Timed out waiting for show buttons to appear.")
    except Exception as e:
        print("An error occurred:", e)


def extract_phone_numbers(driver):
    phone_numbers = []

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'phone-item')))
        phone_items = driver.find_elements(By.CLASS_NAME, 'phone-item')

        for phone_item in phone_items:
            phone_number = phone_item.find_element(By.TAG_NAME, 'span').text.strip()
            phone_numbers.append(phone_number)

    except TimeoutError:
        print("Timed out waiting for phone numbers to appear.")
    except Exception as e:
        print("An error occurred:", e)


def scrape_lalafo_links(start_page, end_page):
    all_links = []

    try:
        for page_number in range(start_page, end_page + 1):
            url = f"https://lalafo.az/azerbaijan/nedvizhimost?page={page_number}"
            response = requests.get(url)

            # Check if the request was successful
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")
            links = soup.find_all("a", href=True)

            for link in links:
                href = link["href"]
                full_link = f'https://lalafo.az{href}'
                all_links.append(full_link)

    except requests.exceptions.RequestException as e:
        print("Request Error:", e)
    except Exception as e:
        print("An error occurred:", e)

    return all_links


def scrape(start_page, end_page, num_buttons_to_click):
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run Chrome WebDriver in headless mode
    driver = webdriver.Chrome(options=chrome_options)

    try:
        all_links = scrape_lalafo_links(start_page, end_page)
        extracted_numbers = []

        for link in all_links:
            try:
                driver.get(link)
                time.sleep(5)
                click_show_buttons(driver, num_buttons_to_click)

                while True:
                    try:
                        phone_numbers = extract_phone_numbers(driver)
                        extracted_numbers.extend(phone_numbers)
                        break  # Break out of the loop if extraction is successful
                    except:
                        continue  # Continue the loop if an exception occurs

            except Exception as e:
                print("An error occurred:", e)

        return extracted_numbers

    finally:
        driver.quit()


start_page = 1
end_page = 2
num_buttons_to_click = 4

extracted_phone_numbers = scrape(start_page, end_page, num_buttons_to_click)

for number in extracted_phone_numbers:
    print(number)
