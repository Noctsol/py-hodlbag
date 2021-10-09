"""
Owner: Kevin B
Contributors: N/A
Date Created: 20210826

Summary:
    This api is really useful for pulling ranking information. I'm not if I'll use the rest of their services though.
    Their historical data offering is crap.

"""

# From PyPi
# from bs4 import BeautifulSoup       # For reading through all our html
# import requests                     # Got sending the request to get the html from a webpage

class CoinMarketCapApi:
    '''Wrapper class around the CMC API'''
    def __init__(self):
        self.base_url = "https://pro-api.coinmarketcap.com"

        # /cryptocurrency services defined by CMC api
        self.listings_latest_url = f"{self.base_url}/v1/cryptocurrency/listings/latest"
        self.category_url = f"{self.base_url}/v1/cryptocurrency/category"
