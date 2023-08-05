from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

def scroll_to_bottom():
    # Scroll to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Wait for some time for new content to load
    time.sleep(3)


def get_property_links(url):
    driver.get(url)
    processed_links = set()
    total_links = 0

    while True:
        soup = BeautifulSoup(driver.page_source, "html.parser")
        properties = soup.find_all('div', class_='AdTileHorizontal')

        for property in properties:
            link = f"lalafo.az{property.a['href']}"
            if link not in processed_links:
                processed_links.add(link)
                total_links += 1
                print(link)

        # Scroll to the bottom to load more content
        scroll_to_bottom()

        # Wait for a short time to let the new properties load (You can adjust the time as needed)
        time.sleep(3)

        # Check if the total number of links remains the same
        soup = BeautifulSoup(driver.page_source, "html.parser")
        properties = soup.find_all('div', class_='AdTileHorizontal')
        if len(properties) == total_links:
            # If no new links found, break the loop
            break

    # End of the loop, scraping finished


if __name__ == "__main__":
    url = "https://lalafo.az/azerbaijan/nedvizhimost"
    get_property_links(url)
    driver.quit()
