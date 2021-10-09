"""
Owner: Kevin B
Contributors: N/A
Date Created: 20210917

Summary:
    Script used to pull all historical data of the top 200 crypto market caps. Will pull everything. Ideally should only be used a couple times or when everything is lost.
"""
# Custom Libraries
from library import coin_market_cap_scrape as cmcs
from library import helper

#
from os.path import expanduser

# Initializing classes
scrape = cmcs.CoinMarketCapScrape()
hlp = helper.Helper()

# Pathing
stamp = hlp.timestamp()
home = expanduser("~")
path = f"{home}/Documents/CryptoAnalytics/"
filepath = f"{path}/historical_crypto_data_{stamp}.csv"
hlp.mkdir(path)

# Body



historical_data_lstdct = scrape.get_all_date_snapshots_data(n_dates_to_pull=0)

historical_data_list = hlp.listdict_to_2dlist(historical_data_lstdct)

hlp.write_to_csv(filepath, historical_data_list)
