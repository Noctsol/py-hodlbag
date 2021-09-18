import sys 
sys.path.append('.')

import requests

from library import environment

env = environment.Environment("./secret/environment.env")
env.load()

api_key = env.get("cryptowatch_key")
print(api_key)

info = requests.get(f"https://api.cryptowat.ch/markets/kraken/btceur/price?apikey={api_key}")

print(info.json())
print(info.status_code)