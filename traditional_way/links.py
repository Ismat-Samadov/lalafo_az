from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

url = "https://lalafo.az/azerbaijan/nedvizhimost"
driver.get(url)

# Initialize a set to store all unique hrefs
all_href_set = set()

# Loop through the pages and extract hrefs
while True:
    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Use BeautifulSoup to find all 'a' elements with href attribute
    href_list = [a['href'] for a in soup.find_all('a', href=True)]

    # Add the new hrefs to the set
    all_href_set.update(href_list)

    # Find the "Next" button and click it if available
    try:
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'paginator-item arrow right')]"))
        )
        if 'disabled' in next_button.get_attribute('class').split():
            # If "Next" button is disabled, exit the loop
            break
        else:
            # Click "Next" button to load the next page
            next_button.click()
            time.sleep(5)  # Wait for content to load (adjust the time as needed)
    except:
        # If the "Next" button is not found or any other exception occurs, exit the loop
        break

driver.quit()

# Create a pandas DataFrame from the all_href_set
df = pd.DataFrame({'URL': list(all_href_set)})

# Save the DataFrame to an Excel file
df.to_excel('output.xlsx', index=False)

# Logging the progress
print(f"Scraped {len(all_href_set)} unique hrefs from {url}")
