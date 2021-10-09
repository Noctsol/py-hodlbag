"""
Owner: Kevin B
Contributors: N/A
Date Created: 20210917

Summary:
    Script used to pull all historical data of the top 200 crypto market caps. Will pull everything. Ideally should only be used a couple times or when everything is lost.
"""



# Preinstalled packages
from os.path import expanduser

# Custom Libraries
from library import coin_market_cap_scrape as cmcs
from library import helper



# Initializing classes
scrape = cmcs.CoinMarketCapScrape()
hlp = helper.Helper()

# Pathing
stamp = hlp.timestamp()
home = expanduser("~")
path = f"{home}/Documents/CryptoAnalytics/historical"

master_filepath = f"{path}/all_historical_crypto_data_{stamp}.csv"

hlp.mkdir(path)

# Body
historical_data_lstdct = scrape.get_all_date_snapshots_data(n_dates_to_pull=0)

# Grouping all data by date
grouped_by_date = {}
for dct in historical_data_lstdct:
    date_key = dct["date"]
    if date_key not in grouped_by_date:
        grouped_by_date[date_key] = []
        grouped_by_date[date_key].append(dct)
    else:
        grouped_by_date[date_key].append(dct)

# Writing data from each date to a csv
for date_key in grouped_by_date:
    data_dicts = grouped_by_date[date_key]
    data_lsts = hlp.listdict_to_2dlist(data_dicts)

    file_date = date_key.replace("-", "")

    filepath = f"{path}/historical_crypto_data_{file_date}.csv"
    hlp.write_to_csv(filepath, data_lsts)

# Writing all data to one file
historical_data_list = hlp.listdict_to_2dlist(historical_data_lstdct)

hlp.write_to_csv(master_filepath, historical_data_lstdct)
