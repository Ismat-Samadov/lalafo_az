import http.client
import json
import csv
import time
import asyncio
import aiohttp
from pandas import json_normalize  # Requires pandas library
from urllib.parse import urlencode

# Global variables
BASE_URL = "https://lalafo.az"
MAX_PAGES = 10  # Set the maximum number of pages to scrape
REQUEST_DELAY = 1  # Set the delay between requests in seconds (to avoid rate limiting)

headers = {
    'cookie': "event_user_hash=47c5933f-9e06-441b-95df-aa57e779cfa9; _gcl_au=1.1.1195818718.1690433739; _fbp=fb.1.1690433774505.1617200774; _gid=GA1.2.12234138.1690964981; _ga=GA1.1.65228442.1690433738; event_session_id=a8d9755534c66917c51aa11976cc7472; lastAnalyticsEvent=home:feed:listing:ad:view; __gads=ID=9b773b1edba435de:T=1690433739:RT=1690973479:S=ALNI_Ma_D5CR_hYxhpqFHAYXE6exm4JN2g; __gpi=UID=00000c47b5691960:T=1690433739:RT=1690973479:S=ALNI_MZzBSc10EYORZ7G9aISJKJk57lq_Q; experiment=novalue; paid-background={%2213-1-0%22:{%22506%22:3}}; device_fingerprint=afe7a4d70a50867f51ddc5988c520c57; _ga_YZ2SWY4MX0=GS1.1.1690972909.13.1.1690973493.0.0.0",
    'authority': "lalafo.az",
    'accept': "application/json, text/plain, */*",
    'accept-language': "en-GB,en-US;q=0.9,en;q=0.8,ru;q=0.7,az;q=0.6",
    'authorization': "Bearer",
    'country-id': "13",
    'device': "pc",
    'dnt': "1",
    'experiment': "novalue",
    'language': "az_AZ",
    'referer': "https://lalafo.az/",
    'request-id': "react-client_a4388b2a-ed9a-4636-8682-6756ac71895c",
    'sec-ch-ua': "\"Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"115\", \"Chromium\";v=\"115\"",
    'sec-ch-ua-mobile': "?0",
    'sec-ch-ua-platform': "\"Windows\"",
    'sec-fetch-dest': "empty",
    'sec-fetch-mode': "cors",
    'sec-fetch-site': "same-origin",
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    'user-hash': "47c5933f-9e06-441b-95df-aa57e779cfa9"
}

async def get_data_from_api(session, page_number):
    url = "/api/search/v3/feed"  # Start the URL with a forward slash
    params = {
        "expand": "url",
        "page": page_number,
        "per-page": 50,
        "vip_count": 5,
        "m-name": "last_push_up",
        "m-next-value": 1690893962285,
        "sub-empty": 1,
    }
    full_url = f"{BASE_URL}{url}?{urlencode(params)}"
    async with session.get(full_url, headers=headers) as response:
        data = await response.read()
        return [data]  # Return data as a list with one element

async def fetch_all_data():
    all_data = []
    async with aiohttp.ClientSession() as session:
        tasks = [get_data_from_api(session, page_number) for page_number in range(1, MAX_PAGES + 1)]
        data_list = await asyncio.gather(*tasks)
        for data in data_list:
            all_data.append(data)
            await asyncio.sleep(REQUEST_DELAY)

    # Join the data as bytes
    combined_data = b"".join(all_data)

    # Split the data into separate JSON objects and decode them one by one
    json_data_list = [json.loads(obj) for obj in combined_data.decode("utf-8").split("}\n{")]

    return json_data_list



async def main():
    start_time = time.time()

    # Fetch all data asynchronously
    all_data = await fetch_all_data()

    # Combine the data chunks into a single list
    combined_data = b"".join(all_data)

    # Convert the data to a list of dictionaries (JSON format)
    json_data = json.loads(combined_data.decode("utf-8"))
    # Extract "url" and "Mobile Number" for every item
    items_info = []
    items = json_data.get("items", [])
    for item in items:
        item_info = {
            "url": item.get("url"),
            "Mobile Number": item.get("mobile"),
        }
        items_info.append(item_info)

    # Save as JSON file
    with open("data_2.json", "w") as json_file:
        json.dump(items_info, json_file)

    # Flatten the JSON data using pandas json_normalize
    flat_data = json_normalize(items_info)

    # Save as CSV file
    flat_data.to_csv("data_2.csv", index=False)

    end_time = time.time()
    print(f"Total execution time: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main())
