"""
Owner: Noctsol
Contributors: N/A
Date Created: 2021-10-30

Summary:
    Backfills data for newly added crypto currencies
"""

# Preinstalled packages
from datetime import datetime, timedelta
from math import ceil
import os
import sys

# From Pypi
import helpu as hlp
import quikenv as qi

# From Project
from library import local_func as lf
from library import ezpostgres as pg
from library import ezmessari as msri


###################################### CONFIG ######################################
# Script configs
env = qi.ezload()
DEBUG = 1
CURRENT_TIME = hlp.timestamp()

# Secrets
DB_CONN_STR = env.get("postgres_conn_str")
MESSARI_KEY = env.get("apikey_messari")

# Classes used
db = pg.Ezpostgres.from_connection_string(DB_CONN_STR)  # Database conn
messari = msri.EzMessari(MESSARI_KEY)                   # Messari API client

###################################### FUNCTIONS ######################################

def print_statuses():
    """Prints out available statuses to use on the DB
    """
    print("AVAILABLE STATUSES")
    if DEBUG == 1:
        query = "SELECT * FROM crypto_status"
        for db_rows in db.select(query):
            print(db_rows)
    print("")

def yesterday():
    """Gets the UTC datetime 24 hours ago"""
    return datetime.utcnow() - timedelta(days=1)

def datetime_to_datestring(my_datetime):
    """Convert a datetime to a date string in YYYY-MM-dd format"""
    return my_datetime.strftime("%Y-%m-%d")

def messari_intervals_to_2009():
    """Return an int that tells me how many calls I need to
    make to look back to 2009-01-01 as this is when, bitcoin,
    the first cryptocurrency was created. This makes the earliest
    possible historical data that could exist
    """
    # This script pulls things in days
    # If you want minute data, give me money and problem solved!~!
    days = (datetime.utcnow() - datetime(2009, 1, 1)).days

    # We use 2016 because this is the max rows messari allows per time interval
    calls_required = ceil(days/2016)

    return calls_required

def calculate_all_messari_intervals():
    """Calculates all the amount of times we need to look back 2016 days
    to get back to 2009-01-01(when it all began)
    """
    n_messari_calls = messari_intervals_to_2009()
    interval_strings = []

    # Get yesterdays datetime (24h ago)
    lookback_time = yesterday()

    # Calculate time ranges of 2010 days to get back to 2009-01-01
    for _ in range(n_messari_calls):

        # Lookback for next time inv
        new_times = lf.calculate_interval_datetimes(timestamp=lookback_time)

        # Convert datetime to strings
        interval_tuple = (datetime_to_datestring(new_times[0]), datetime_to_datestring(new_times[1]))
        interval_strings.append(interval_tuple)

        # Set new time to look back(minus 1 day to avoid duplicate data)
        lookback_time = new_times[0] - timedelta(days=1)

    return interval_strings

def backfill_messari_timeseries(crypto_name, messari_metric_id, time_intervals):
    """Gets all the price OHLCV data for a crytocurrency on messari.io"""

    messari_timeseries_data = []

    # Executing all api calls and extracting info
    for start_time, end_time in date_pairs:
        # Making api call
        response = messari.get_asset_timeseries(crypto_name, messari_metric_id, start_time, end_time)

        if response.status_code == 429:
            # Do some kind of sleep here
            pass
        elif response.status_code not in (200, 429):
            # Throw exception here
            pass

        # Converting data to a flat dictionary
        flat_dict = messari.extract_timeseries(response)
        # This means messari has no data on this item
        if flat_dict is None:
            continue

        # Add data to container
        messari_timeseries_data+=messari.extract_timeseries(response)

    return messari_timeseries_data

###################################### BODY ######################################

# DEBUG FUNCTIONS
if DEBUG == 1:
    print_statuses()
    lf.test_timeframes()

# Required times to look back to 2009-01-01 in chunks of 2016 days (for messari)
date_pairs = calculate_all_messari_intervals()
print(date_pairs)

# Back filling OHL
messari_price_timeseries_data = backfill_messari_timeseries("nano", "price", date_pairs)

for i in messari_price_timeseries_data:
    print(i)

