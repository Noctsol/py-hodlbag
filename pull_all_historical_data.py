"""
Owner: Noctsol
Contributors: N/A
Date Created: 20210917

Summary:
    Script to use all historical snapshots. Will pull from scratch if need be. Will backfill anything that is missing.
"""



# Preinstalled packages
from datetime import datetime
from os.path import expanduser
import os
import pathlib


# Custom Libraries
from library import coin_market_cap_scrape as cmcs
import helpu as hlp



############################################## CONFIG ##############################################

# Initializing classes
scrape = cmcs.CoinMarketCapScrape()
# hlp = helper.Helper()

# Pathing
stamp = hlp.timestamp()
home = expanduser("~")
download_dir = f"{home}/Documents/CryptoAnalytics/historical/"
aggrate_dir = f"{download_dir}aggregate"
stats_dir = f"{download_dir}stats"

FILE_NAME_PREFIX = "historical_snapshot_"
FILE_NAME_AGG = "aggregate_historical_snapshot.csv"
FILE_NAME_TOTAL_CAP = "crypto_total_market_cap.csv"
FILE_NAME_UNIQUE = "unique_cryptos.csv"

# Making directories
hlp.mkdir(download_dir)
hlp.mkdir(aggrate_dir)
hlp.mkdir(stats_dir)

# Debug
DEBUG_MODE_ON = False
DEBUG_PAGES = 3
DEBUG_COUNTER = 0

# No Category
cmc_200_datetime = datetime(2014, 3, 30)  # Anything on this date or greater should return 200 total assets


############################################## FUNCTIONS ##############################################

# Checks if a given file string is the correct format and file type
def is_downloaded_file(f_name):
    ''' Check if a file has the correct name prefix and is a csv file type'''
    if not f_name.startswith(FILE_NAME_PREFIX) and pathlib.Path(f_name).suffix != ".csv":
        return False
    return True

# Checks the download directory to see which files have already been downloaded
def get_downloaded_dates():
    ''' Get a list of dates we already have data for'''
    dl_dates = set()

    downloaded_files = os.listdir(download_dir)
    for i in downloaded_files:
        # Ignore anything that isn't a csv file starting with historical_snapshot_
        if not is_downloaded_file(i):
            continue

        # Strip the datetime
        file_datetime = datetime.strptime(i, f"{FILE_NAME_PREFIX}%Y%m%d.csv")

        # Add to set
        dl_dates.add(file_datetime)

    return dl_dates

# Takes all the downlaoded files and merges then into one aggregates file
def aggregate_data_from_files():
    ''' Cycles through entires downloaded_dir and reads all the files and aggregates the data
        into one file'''

    all_historical_data = []

    downloaded_files = os.listdir(download_dir)
    for i in downloaded_files:
        # Ignore anything that isn't a csv file starting with historical_snapshot_
        if not is_downloaded_file(i):
            continue

        print(f"Reading {i}")

        # Reading CSV file
        crypto_data_lsts = hlp.read_csv(os.path.join(download_dir, i))

        # Append header once
        if len(all_historical_data) == 0:
            all_historical_data.append(crypto_data_lsts[0])

        # Adding data to
        all_historical_data+=crypto_data_lsts[1:]

    return all_historical_data

def generate_total_market_cap_file(all_combined_data):
    ''' Generates a csv totaling the total market cap '''

    headers = ["date", "Cryto200"]
    market_cap_data = [headers]

    # Grouping data
    grouped_by_date = {}
    for row in all_combined_data[1:]:
        if row[0] not in grouped_by_date:
            grouped_by_date[row[0]] = []
            grouped_by_date[row[0]].append(row)
        else:
            grouped_by_date[row[0]].append(row)

    # Sum data
    for d_key in grouped_by_date:
        rows = grouped_by_date[d_key]

        temp_lst = [d_key]
        date_market_cap_total = 0

        for row in rows:
            coin_market_cap = float(row[4])
            date_market_cap_total+=coin_market_cap

        temp_lst.append(date_market_cap_total)
        market_cap_data.append(temp_lst)

    hlp.write_csv(os.path.join(stats_dir,FILE_NAME_TOTAL_CAP), market_cap_data)

def generate_unique_crypto_file(all_combined_data):
    ''' Generates a csv with all the unique symbol,name pairs '''

    dict_set = {}

    for row in all_combined_data[1:]:
        name = row[2].lower()
        symbol = row[3].lower()

        if name not in dict_set:
            dict_set[name] = symbol
        else:
            # Here to deal with cases where the acronym changes
            # We take the most recent acronym
            if name in dict_set and symbol != dict_set[name]:
                dict_set[name] = symbol
            else:
                continue

    unique_pairs = [[i, dict_set[i]] for i in dict_set]

    headers = ["name", "symbol"]
    output = [headers] + unique_pairs

    hlp.write_csv(os.path.join(stats_dir,FILE_NAME_UNIQUE), output)



############################################## BODY ##############################################

# Get snapshots dates available
available_snapshot_dates_on_cmc = scrape.get_available_historical_snapshots()

# Extracting dates from files already downloaded
downloaded_dates = get_downloaded_dates()

# Webscraping data from coin market cap
for date_key in available_snapshot_dates_on_cmc:

    info = available_snapshot_dates_on_cmc[date_key]
    datestamp = info["date"]

    # Skip if we already downlaoded this file
    if date_key in downloaded_dates:
        print(f"SKIPPING - {datestamp} - Already downloaded")
        continue

    # Getting data from CMC
    print(f"PULLING - {datestamp}", end=" ")
    data_lstdct = scrape.get_date_snapshot_data(datestamp)

    # Sanity check based on functional knowledge
    if date_key >= cmc_200_datetime and len(data_lstdct) < 200:
        raise Exception("Missing data from webscraped page. Should be a total of 200 coins.")

    print(f"\t#OF COINS: {len(data_lstdct)}")

    # Transforming to nested list
    data_lsts = hlp.to_listlist(data_lstdct)

    # Removing dashes from datestamp for filename
    file_datestamp = datestamp.replace("-","")
    file_name = f"{FILE_NAME_PREFIX}{file_datestamp}.csv"
    file_out_path = f"{download_dir}{file_name}"

    # Write to csv
    hlp.write_csv(file_out_path, data_lsts)

    # End script early on DEBUG mode
    if DEBUG_MODE_ON is True:
        DEBUG_COUNTER+=1
        if DEBUG_COUNTER == DEBUG_PAGES:
            break

# Take all files in the historical dir and combine
combined_data = aggregate_data_from_files()

# Write to csv
hlp.write_csv(os.path.join(aggrate_dir, FILE_NAME_AGG),combined_data)

# Generate Stats
generate_total_market_cap_file(combined_data)
generate_unique_crypto_file(combined_data)

print("\nScript Complete - Exiting")
