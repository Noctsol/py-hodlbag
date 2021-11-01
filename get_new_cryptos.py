"""
Owner: Noctsol
Contributors: N/A
Date Created: 2021-10-30

Summary:
    Inserts new crypto into the asset table

    - new - newly inserted asset
    - backfilling
    -
"""

# Preinstalled packages


# From pypi
from logging import info
import requests
import helpu
import quikenv


env = quikenv.ezload()
apikey = env.get("apikey_messari")

headers = {
    "x-messari-api-key": apikey
}

metric_params = {
    "page1": "1",
    "limit": "500",
    "with-metrics": True
}

profile_params = {
    "page": "1",
    "limit": "500",
    "with-profiles": True
}

metricprofile_params = {
    "page": "1",
    "limit": "500",
    "with-metrics": "any",
    "with-profiles": "any"
}

url = "https://data.messari.io/api/v2/assets"

# resp_metrics = requests.get(url, headers=headers, params=metric_params)
# resp_profile = requests.get(url, headers=headers, params=metric_params)
resp_both = requests.get(url, headers=headers, params=metricprofile_params)
print(resp_both.request.url)

def print_info(response):
    data = response.json()["data"]
    print(f"Total Assets: {len(data)}")
    for dct in data:
        print(dct["name"])

# print_info(resp_metrics)
# print("\n")
# print_info(resp_profile)
# print("\n")
print_info(resp_both)
print("\n")

# for i in range(65):
#     resp = requests.get(url, headers=headers, params=params)
#     print(resp.status_code)
#     if resp.status_code != 200:
#         print(f"attempt:{i+1}")
#         print(resp.request.headers)
#         print(resp.json())
#         break




