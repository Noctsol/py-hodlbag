import sys 
sys.path.append('.')


import requests
from library import environment


env = environment.Environment("./secret/environment.env")
env.load()

api_key = env.get("coinmarketcap_key")
url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

headers = {
    "X-CMC_PRO_API_KEY": api_key
}
params = {"limit": "20"}


# api_request = requests.get(url, headers=headers, params=params)



api_request_json =  {'status': {'timestamp': '2021-09-25T00:56:30.082Z', 'error_code': 0, 'error_message': None, 'elapsed': 8, 'credit_count': 1, 'notice': None, 'total_count': 6818}, 'data': [{'id': 1, 'name': 'Bitcoin', 'symbol': 'BTC', 'slug': 'bitcoin', 'num_market_pairs': 8681, 'date_added': '2013-04-28T00:00:00.000Z', 'tags': ['mineable', 'pow', 'sha-256', 'store-of-value', 'state-channels', 'coinbase-ventures-portfolio', 'three-arrows-capital-portfolio', 'polychain-capital-portfolio', 'binance-labs-portfolio', 'arrington-xrp-capital', 'blockchain-capital-portfolio', 'boostvc-portfolio', 'cms-holdings-portfolio', 'dcg-portfolio', 'dragonfly-capital-portfolio', 'electric-capital-portfolio', 'fabric-ventures-portfolio', 'framework-ventures', 'galaxy-digital-portfolio', 'huobi-capital', 'alameda-research-portfolio', 'a16z-portfolio', '1confirmation-portfolio', 'winklevoss-capital', 'usv-portfolio', 'placeholder-ventures-portfolio', 'pantera-capital-portfolio', 'multicoin-capital-portfolio', 'paradigm-xzy-screener'], 'max_supply': 21000000, 'circulating_supply': 18825281, 'total_supply': 18825281, 'platform': None, 'cmc_rank': 1, 'last_updated': '2021-09-25T00:55:02.000Z', 'quote': {'USD': {'price': 42716.18257653351, 'volume_24h': 42833508490.41135, 'percent_change_1h': -0.0858924, 'percent_change_24h': -4.38903416, 'percent_change_7d': -9.53554115, 'percent_change_30d': -13.43814735, 'percent_change_60d': 14.63042156, 'percent_change_90d': 32.12848408, 'market_cap': 804144140250.5474, 'market_cap_dominance': 42.0595, 'fully_diluted_market_cap': 897039834107.2, 'last_updated': '2021-09-25T00:55:02.000Z'}}}]}


data = api_request_json["data"]


for crypto in data:
    lst = [crypto["id"], crypto["name"], crypto["quote"]["USD"]["price"]]
    print(lst)