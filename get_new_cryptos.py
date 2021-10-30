"""
Owner: Noctsol
Contributors: N/A
Date Created: 2021-10-30

Summary:
    Inserts new crypto into the asset table
"""

# Preinstalled packages


# From pypi
import requests
import helpu
import quikenv


env = quikenv.ezload()
apikey = env.get("apikey_messari")

headers = {
    "x-messari-api-key": apikey
}

params = {
    "pages": "1",
    "limit": "1",
    "with_metrics": True
}

url = "https://data.messari.io/api/v2/assets"

for i in range(65):
    resp = requests.get(url, headers=headers, params=params)
    print(resp.status_code)
    if resp.status_code != 200:
        print(f"attempt:{i+1}")
        print(resp.request.headers)
        print(resp.json())
        break


