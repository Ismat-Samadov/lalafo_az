import http.client
import json
import csv
from pandas import json_normalize  # Requires pandas library


def get_data_from_api(page_number):
    conn = http.client.HTTPSConnection("lalafo.az")
    payload = ""
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

    url = f"/api/search/v3/feed?expand=url&page={page_number}&per-page=100&vip_count=5&m-name=last_push_up&m-next-value=1690893962285&sub-empty=1"
    conn.request("GET", url, payload, headers)
    try:
        res = conn.getresponse()
        data = res.read()
        return data
    except http.client.IncompleteRead as e:
        # Retry the request in case of an incomplete read
        return e.partial


all_data = []
current_page = 1

while True:
    data = get_data_from_api(current_page)
    if not data:
        break  # Stop the loop when no data is returned
    all_data.append(data)
    current_page += 1

# Convert the data to a list of dictionaries (JSON format)
json_data = [json.loads(data.decode("utf-8")) for data in all_data]

# Save as JSON file
with open("data.json", "w") as json_file:
    json.dump(json_data, json_file)

# Flatten the JSON data using pandas json_normalize
flat_data = json_normalize(json_data)

# Save as CSV file
flat_data.to_csv("data.csv", index=False)
