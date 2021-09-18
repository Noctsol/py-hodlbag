import sys 
sys.path.append('.')


from library import coin_market_cap_scrape as cmcs


scrape = cmcs.CoinMarketCapScrape()

years_content = scrape.get_eligible_historical_info()

# for i in years_content:
#     print(scrape.get_year_text(i))

