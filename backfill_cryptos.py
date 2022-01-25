"""
Owner: Noctsol
Contributors: N/A
Date Created: 2021-10-30

Summary:
    Backfills data for newly added crypto currencies
"""
import time

# From Pypi
import helpu as hlp
import quikenv as qi

# From Project
from library import hodlbag_spider
from library import hodlbag_databot


###################################### CONFIG ######################################
# Script configs
env = qi.ezload()
DEBUG = 1
CURRENT_TIME = hlp.timestamp()

# Secrets
DB_CONN_STR = env.get("postgres_conn_str")
MESSARI_KEY = env.get("apikey_messari")

# Classes used
# db = pg.Ezpostgres.from_connection_string(DB_CONN_STR)  # Database conn
# messari = msri.EzMessari(MESSARI_KEY)                   # Messari API client
spider = hodlbag_spider.HodlbagSpider(MESSARI_KEY)
databot = hodlbag_databot.HodlbagDatabot(DB_CONN_STR)

###################################### FUNCTIONS ######################################
def prt(string):
    """Wrapper around print() to only print if DEBUG == 1
    """
    if DEBUG == 1:
        print(string)




###################################### BODY ######################################

# DEBUG FUNCTIONS
if DEBUG == 1:
    databot.get_cstatus()
    databot.get_cts_status()
    spider.test_timeframes()

# new_cryptos = databot.get_new_cryptos()
new_cryptos = databot.get_new_cryptos_test()

for i in new_cryptos:
    print(i)


# Required times to look back to 2009-01-01 in chunks of 2016 days (for messari)
date_pairs = spider.calculate_all_messari_intervals()
date_pairs = [date_pairs[0]]

import datetime
date_pairs = [(datetime.datetime(2021,11, 1), datetime.datetime(2021,11, 3))]



messari_metrics = ["price", "sply.circ", "sply.out", "mcap.out"]
metric_data = {}
sources = ["https://messari.io/"]

# # Back filling OHLCV
for cryptodct in new_cryptos:
    crypto_name = cryptodct["crypto_name"]
    symbol = cryptodct["symbol"]
    crypto_id = cryptodct["crypto_id"]

    prt(f"Pulling data for {crypto_name}")

    # Get profile
    profile_data = spider.get_messari_profile(crypto_name)
    print(profile_data)

    # # Pulling different metrics from messari
    # for metric in messari_metrics:
    #     prt(f"Pulling pulling {metric}")
    #     timeseries_data = spider.backfill_messari_timeseries(crypto_name, metric, date_pairs)
    #     prt(timeseries_data)



# print(messari_price_ts_data)
# # for i in messari_price_ts_data:
# #     print(i)

# print(databot.messari_timeseries_insert_statement("price", 5, messari_price_ts_data, sources))


# messari_price_timeseries_data = spider.backfill_messari_timeseries("nano", "price", date_pairs)
# messari_price_timeseries_data = spider.backfill_messari_timeseries("nano", "price", date_pairs)
