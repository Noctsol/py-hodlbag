"""
Owner: Noctsol
Contributors: N/A
Date Created: 2021-10-30

Summary:
    Inserts new crypto into the asset table, this pulls from coin market cap

"""


# From repo
from library import ezpostgres

# Preinstalled packages
import sys

# From Pypi
import requests
# import helpu
import quikenv

############################### CONFIG ###############################
env = quikenv.ezload()

# API Constants
APIKEY_CMC = env.get("apikey_coinmarketcap")
URL_CMC = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
HEADER_CMC = {"X-CMC_PRO_API_KEY": APIKEY_CMC}
PARAMS_CMC = {"limit":200}

# DB info
DB_STR = env.get("postgres_conn_str")
CRYPTO_QUERY = "SELECT crypto_name FROM crypto AS cry WHERE cry.ccategory_id = 1"

# Will hold any net new cryptos not in DB
new_cryptos = []
already_exists = set()


############################### CONFIG ###############################
# Converts the json pull from CMC to an insert string
def to_insert_string(new_crypto_dicts):
    """Converts the json pull from CMC to an insert string

    Args:
        new_crypto_dicts (listdict): Dictionaries embedded inside "data" section
    """
    insert_rows = []

    for fdct in new_crypto_dicts:
        cname = fdct["name"].lower()
        symbol = fdct["symbol"].lower()
        insert_row_string = f"('{cname}', '{symbol}', 1, 1, '{{{URL_CMC}}}')"
        insert_rows.append(insert_row_string)

    insert_rows_string = ",".join(insert_rows)

    generated_insert_statement = ("INSERT INTO crypto(crypto_name, symbol, ccategory_id, cstatus_id, sources)"
        f"\nVALUES\n{insert_rows_string};")

    return generated_insert_statement

############################### BODY ###############################

### GET RECENT LISTINGS FFROM COIN MARKET CAP

### Call API and check response
response = requests.get(URL_CMC, headers=HEADER_CMC, params=PARAMS_CMC)
if response.status_code != 200:
    print(response.json())
    raise Exception("Please buy me a Splunk license")

#  Convert response body to json
crypto_listings_json = response.json()["data"]


### GET RECENT LISTINGS FROM COIN MARKET CAP

# Connect to db and pull data
conn = ezpostgres.Ezpostgres.from_connection_string(DB_STR)
existing_cryptos = conn.select(CRYPTO_QUERY)

# Turn data into set
for dct in existing_cryptos:
    already_exists.add(dct["crypto_name"])


### COMPARE AND INSERT NEW CRYPTOS

# Getting any new cryptos that have shown up
for crypto_dct in crypto_listings_json:
    crypto_name = crypto_dct["name"].lower()
    if crypto_name not in already_exists:
        new_cryptos.append(crypto_dct)

# END script if no new items are in
if len(new_cryptos) == 0:
    print("END - No new cryptos to add")
    sys.exit()
else:
    print(f"Total NEW: {len(new_cryptos)}")
    _ = [print(i) for i in new_cryptos]

# Converting stored JSON
insert_statement = to_insert_string(new_cryptos)

# Inserting new records
try:
    new_cursor = conn.dbconn.cursor()
    new_cursor.execute(insert_statement)
    conn.dbconn.commit()
finally:
    new_cursor.close()
    conn.dbconn.close()

print("END - Script complete")
