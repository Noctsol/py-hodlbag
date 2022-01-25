"""
Owner: Noctsol
Contributors: N/A
Date Created: 2021-11-06

Summary:
    Class made to access the primary db and quickly pull/insert
"""


# Preinstalled packages
from datetime import datetime, timedelta

from helpu.helpu import timestamp

# From Pypi


# From Project
from . import ezpostgres



class HodlbagDatabot:
    """Class made to access the primary db and quickly pull/insert"""
    def __init__(self, db_conn_string):
        self.db_conn_string = db_conn_string
        self.ezpg = ezpostgres.Ezpostgres.from_connection_string(db_conn_string)
        self.messari_map = {
            "price": {
                "table": "cts_price",
                "field": {
                    "timestamp": "record_time",
                    "open": "open_price",
                    "high": "high_price",
                    "low": "low_price",
                    "close":"close_price",
                    "volume": "volume"
                }
            },
            "sply.circ":{
                "table": "cts_circulating_supply",
                "field": {
                    "timestamp": "record_time",
                    "circulating_supply": "circulating_supply",
                }
            },
            "sply.out":{
                "table": "cts_outstanding_supply",
                "field": {
                    "timestamp": "record_time",
                    "oustanding_supply": "oustanding_supply",
                }
            },
            "mcap.out":{
                "table": "cts_outstanding_mcap",
                "field": {
                    "timestamp": "record_time",
                    "oustanding_marketcap": "oustanding_marketcap",
                }
            }
        }


    ###################################### PUBLIC ######################################

    def get_cts_status(self, should_print=True):
        """Gets all the base cts time series statuses"""
        query = "SELECT cts_status_id, cts_status_name, long_description FROM cts_status"
        data = self.ezpg.select(query)
        if should_print is True:
            print("AVAILABLE CTS STATUSES")
            for dct in data:
                print(dct)
            print("")

    def get_cstatus(self, should_print=True):
        """Gets all the base Crypot Statuses"""
        query = "SELECT cstatus_id, cstatus_name, long_description FROM cstatus"
        data = self.ezpg.select(query)
        if should_print is True:
            print("AVAILABLE CRYPTO STATUSES")
            for dct in data:
                print(dct)
            print("")

        return data

    def get_new_cryptos(self):
        """ Gets all the crypto in the new (1) status """
        query = """
            SELECT crypto_name, alternate_name, symbol, crypto_id
            FROM crypto
            WHERE ccategory_id = 1 AND cstatus_id = 1
        """
        return self.ezpg.select(query)

    def get_new_cryptos_test(self):
        """ Test function pull nano and a crypto that will amost certainly have no fucking data """
        query = """
            SELECT crypto_name, alternate_name, symbol, crypto_id
            FROM crypto
            WHERE ccategory_id = 1 AND cstatus_id = 1
                AND crypto_id IN (5, 22)
        """
        return self.ezpg.select(query)

    def lst_to_pgarray(self, lst):
        """Recursive function to convert a python list of a pg string array for inserting

        Args:
            lst (list): list with generic default python types

        Returns:
            string: ex. {{1,2},{"my","dog"},{"is","supercute"}}
        """
        postgres_insert_strings = []

        for i in lst:
            new_value = i
            if isinstance(i, list):
                new_value = self.lst_to_pgarray(i)
            elif isinstance(i, str):
                new_value = f"\"{i}\""
            elif isinstance(i, datetime):
                new_value = i.strftime("timestamp '%Y-%m-%d %H:%M:%S'")
            else:
                new_value = str(i)

            postgres_insert_strings.append(new_value)

        joined = ",".join(postgres_insert_strings)
        pg_string = f"'{{{joined}}}'"

        return pg_string

    def to_pgvalue(self, value):
        new_value = value
        if isinstance(value, list):
            new_value = self.lst_to_pgarray(value)
        elif isinstance(value, str):
            new_value = f"\"{value}\""
        elif isinstance(value, datetime):
            new_value = value.strftime("timestamp '%Y-%m-%d %H:%M:%S'")
        else:
            new_value = str(value)

        return new_value

    def to_timeseries_row_repr(self, metric_name, crypto_id, cts_status_id, sources_lst, values_dict):
        """Generates a dictionary representing a timeseries table

        Args:
            crypto_id (int): Integer representing a status on the cstatus table
            cts_status_id (int): integer repsenting a status on cts_status table
            sources_lst (list): list of strings ["http://mysourcesite.com"]
            values_dict (dict): values for this table

        Returns:
            dict: ex.
        """
        #TODO:  expose mapping if i get mroe sources
        mapping = self.messari_map[metric_name]
        table_name =  mapping["table"]
        field_map = mapping["field"]

        # Setting default values in every timeseries table
        mapped_values_dict = {
            "table_name": table_name,
            "crypto_id": crypto_id,
            "cts_status_id": cts_status_id,
            "sources": sources_lst
        }

        # Setting custom metrics
        for kname in values_dict:
            field_name = field_map[kname]
            value = values_dict[kname]
            mapped_values_dict[field_name] = value

        return mapped_values_dict

    def to_timeseries_row_string(self, ts_repr_dict):
        """Converts a representation of the timeseries row to an insert string"""

        values_lst = []

        # Cycle through values
        for key in ts_repr_dict:
            # Skip if table name
            if key == "table_name":
                continue

            # Convert value to insert string format
            pgvalue =  self.to_pgvalue(ts_repr_dict[key])

            # Append to list
            values_lst.append(pgvalue)

        # Join values into comma separated string
        joined = ",".join(values_lst)

        return f"({joined})"

    def to_timeseries_row_strings(self, list_of_ts_repr_dict):
        """Calls self.to_timeseries_row_string() on many dicts in a list"""

        row_lst = []

        # Cycle through dicts and convert them to insert hows
        for dct in list_of_ts_repr_dict:
            row_lst.append(self.to_timeseries_row_string(dct))

        # Join all rows into a comma separated string
        joined = ",".join(row_lst)
        formatted = f"VALUES {joined};"

        return formatted

    def to_timeseries_insert_header(self, ts_repr_dict):
        """Converts a representation of the timeseries row to an insert header
            Ez. INSERT INTO table(fields...)
        """

        values_lst = []

        # Cycle through values
        for key in ts_repr_dict:
            # Skip if table name
            if key == "table_name":
                continue

            # Append to list
            values_lst.append(key)

        # Join values into comma separated string
        joined = ",".join(values_lst)
        table_name =  ts_repr_dict["table_name"]

        insert_header = f"INSERT INTO {table_name} ({joined})"

        return insert_header

    def to_timeseries_insert_statement(self, list_of_ts_repr_dict):
        """Generates a full insert statement to run into a timeseries table

        Args:
            list_of_ts_repr_dict (list): list of dictionaries

        Returns:
            string: a full blow insert statement
        """
        insert_header = self.to_timeseries_insert_header(list_of_ts_repr_dict[0])
        insert_values = self.to_timeseries_row_strings(list_of_ts_repr_dict)

        insert_statement = f"{insert_header} {insert_values}"

        return insert_statement


    def messari_timeseries_insert_statement(self, metric_name, crypto_id, json_lst_dct, sources_lst):

        row_reprentations = []

        # cts status id 1 = closed
        # cts status id 3 = dubious

        # Getting date from a week ago
        # Anything a week old will have a cts_status_id of 3 as it is not necessarily finalized
        #
        time_1week_ago = datetime.utcnow() - timedelta(days=7)


        # Convert results from API calls to dicts representing rows
        for dct in json_lst_dct:
            # Assume that data is dubious (id 3 = dubious) by deefault
            cts_status_id = 3

            # If data is older than time_1week_ago, we consider it finalized (id 1 = closed)
            if time_1week_ago > dct ["timestamp"]:
                cts_status_id = 1

            # Convert to representation of row
            row_repr = self.to_timeseries_row_repr(metric_name, crypto_id, cts_status_id, sources_lst, dct)

            row_reprentations.append(row_repr)

        # Generate insert statement
        timeseries_insert_statement = self.to_timeseries_insert_statement(row_reprentations)

        return timeseries_insert_statement





    ###################################### PRIVATE ######################################
