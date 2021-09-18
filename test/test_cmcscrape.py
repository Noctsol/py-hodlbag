import sys 
sys.path.append('.')


from library import coin_market_cap_scrape as cmcs


scrape = cmcs.CoinMarketCapScrape()

available_snapshots = scrape.get_available_historical_snapshots()

# for i in years_content:
#     print(scrape.get_year_text(i))

for dt_key in available_snapshots:
    info = available_snapshots[dt_key]
    print(dt_key, info)


