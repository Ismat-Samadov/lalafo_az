import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def get_updated_html(url):
    # Set up the Chrome WebDriver (make sure you have Chrome installed and the corresponding chromedriver in your PATH)
    driver = webdriver.Chrome()
    driver.get(url)

    # Wait for the "show-button" elements to appear (up to 10 seconds)
    show_buttons = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "show-button"))
    )

    # Click the "Göstər" button for all phone numbers (phone-number__with-social elements)
    for show_button in show_buttons:
        show_button.click()
        time.sleep(2)  # Adjust the wait time based on the website's speed

    # Wait for a few seconds to allow the content to load (you may need to adjust the wait time based on the website's speed)
    time.sleep(5)

    # Get the updated HTML content after clicking the buttons
    updated_html = driver.page_source

    # Close the WebDriver
    driver.quit()

    return updated_html

def extract_data(html_content):
    soup = BeautifulSoup(html_content, "html.parser")

    # Find all phone number divs
    phone_number_divs = soup.find_all("div", class_="phone-number__wrap")

    # Extract phone numbers
    phone_numbers = []
    for phone_number_div in phone_number_divs:
        phone_number = phone_number_div.find("span", class_="phone-wrap").text.strip()
        phone_numbers.append(phone_number)

    return phone_numbers

def main():
    url = "https://lalafo.az/baku/ads/baki-hovsan-qs-74-kv-m-3-otaqli-hovuzsuz-kombi-qaz-isiq-id-92773245"
    updated_html = get_updated_html(url)
    phone_numbers = extract_data(updated_html)

    # Print or do whatever you want with the extracted data
    for phone_number in phone_numbers:
        print("Phone number:", phone_number)

if __name__ == "__main__":
    main()
