import sys 
sys.path.append('.')


from library import coin_market_cap_scrape as cmcs
from library import helper


scrape = cmcs.CoinMarketCapScrape()
hlp = helper.Helper()


def test_frontpage_scrape():
    available_snapshots = scrape.get_available_historical_snapshots()


    for dt_key in available_snapshots:
        info = available_snapshots[dt_key]
        print(dt_key, info)


data = scrape.get_all_date_snapshots_data()

print(hlp.listdict_to_2dlist(data))
