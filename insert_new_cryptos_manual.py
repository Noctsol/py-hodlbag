"""
Owner: Noctsol
Contributors: N/A
Date Created: 2021-11-02

Summary:
    Manually insert new crypto currencies from a csv file

"""


# From repo
from library import ezpostgres

# Preinstalled packages
import sys

# From Pypi
import helpu
import quikenv


############################### CONFIG ###############################
env = quikenv.ezload()

UNIQUE_CSV = env.get("unique_cryptos_csv")

# DB info
DB_STR = env.get("postgres_conn_str")
CRYPTO_QUERY = "SELECT crypto_name FROM crypto AS cry WHERE cry.category_id = 1"

# Will hold any net new cryptos not in DB
new_cryptos = []
already_exists = set()


############################### CONFIG ###############################
# Converts the json pull from CMC to an insert string
def to_insert_string(new_crypto_lists):
    """Converts the json pull from CMC to an insert string

    Args:
        new_crypto_dicts (listdict): Dictionaries embedded inside "data" section
    """
    insert_rows = []

    for lst in new_crypto_lists:
        cname = lst[0].lower()
        symbol = lst[1].lower()
        insert_row_string = f"('{cname}', '{symbol}', 1, 1)"
        insert_rows.append(insert_row_string)

    insert_rows_string = ",".join(insert_rows)

    generated_insert_statement = ("INSERT INTO crypto(crypto_name, symbol, category_id, crypto_status_id)"
        f"\nVALUES\n{insert_rows_string};")

    return generated_insert_statement

############################### BODY ###############################

### READ CSV FILE

### Call API and check response
csv_data = helpu.read_csv(UNIQUE_CSV)[1:]

# Connect to db and pull data
conn = ezpostgres.Ezpostgres.from_connection_string(DB_STR)
existing_cryptos = conn.select(CRYPTO_QUERY)

# Turn data into set
for dct in existing_cryptos:
    already_exists.add(dct["crypto_name"])


### COMPARE AND INSERT NEW CRYPTOS

# Getting any new cryptos that have shown up
for row in csv_data:
    crypto_name = row[0]
    if crypto_name not in already_exists:
        new_cryptos.append(row)

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
    new_cursor = conn.psy_conn.cursor()
    new_cursor.execute(insert_statement)
    conn.psy_conn.commit()
finally:
    new_cursor.close()
    conn.psy_conn.close()

print("END - Script complete")
