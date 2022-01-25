"""
Owner: Noctsol
Contributors: N/A
Date Created: 2021-10-30

Summary:
    Quick class made to access messari.io's api client. I only wrote functionality for what I used
"""

# Preinstalled packages
from datetime import datetime

# From Pypi
import requests

# From Project


class EzMessari:
    """Class made to access Messari.io's API Client.
        You can initialize this class with/without an api key
    """
    def __init__(self, apikey=None):
        self.base_url = "https://data.messari.io"
        self.api_key = apikey

        # Start session and add api key header if available
        self.session = requests.Session()
        if self.api_key is not None:
            self.session.headers.update({'x-messari-api-key': self.api_key})

    ###################################### PUBLIC ######################################

    ################ TIME SERIES ################
    def get_asset_timeseries(
        self,
        asset_key,
        metric_id,
        start,
        end,
        interval="1d",
        columns=None,
        order="ascending",
        time_format="rfc3339"
        ):
        """Retrieve historical timeseries data for an asset

        Args:
            asset_key (str): This "key" can be the asset's ID (unique), slug (unique), or symbol (non-unique)
            metric_id (str): The metricID is a unique identifier which determines which columns are returned
                by time-series endpoints. For a list of valid metric ids, check the API response at
                https://data.messari.io/api/v1/assets/metrics.

            start (str): Datetime string in the "YYYY-MM-DD" format. The "start" query parameter
                can be used to set the date that points are returned after.
            end (str): Datetime string in the "YYYY-MM-DD" format. The "end" query parameter can be
                used to set the date after which no more points will be returned.
            interval (str, optional): Defines what interval the resulting points will be returned in.
                Possible values are "1m" "5m" "15m" "30m" "1h" "1d" "1w". Defaults to "1d".
            columns (str, optional): A comma separated list of strings that controls which
                columns will be returned and in what order. Defaults to None.
            order (str, optional): Order controls whether points in the response are returned
                in ascending or descending order. Possible values are "ascending" "descending".
                Defaults to "ascending".
            time_format (str, optional): timestamp format returned. Possible values are
                "unix-millisecond" "unix-second" "rfc3339". Defaults to "rfc3339".

        Returns:
            object: a python requests object
        """
        # Forming path
        path = f"/api/v1/assets/{asset_key}/metrics/{metric_id}/time-series"

        # Generating params
        parameters = {
            "start": start,
            "end": end,
            "interval": interval,
            "order": order,
            "timestamp-format": time_format,
            "format": "json"
        }

        # Add columns param if exists
        if columns is not None:
            parameters["columns"] = columns

        return self._get(path, parameters=parameters)

    def get_price_timeseries(
        self,
        asset_key,
        start,
        end,
        interval="1d",
        order="ascending",
        time_format="rfc3339"
        ):
        """Retrieve historical OHLCV timeseries data for an asset
        Refer to get_asset_timeseries() for documentation

        Returns:
            object: a python requests object
        """

        metric_id = "price"

        response = self.get_asset_timeseries(
            asset_key,
            metric_id,
            start,
            end,
            interval=interval,
            columns=None,
            order=order,
            time_format=time_format
        )
        print(response.request.url)
        return response

    def extract_timeseries(self, timeseries_response):
        """Extracts the data from timeseries json into a simple dict

        Args:
            timeseries_response (str): Response from the Messari timeseries method

        Returns:
            list: A list containing flat dictionaries
        """
        timeseries_json = timeseries_response.json()
        columns = timeseries_json["data"]["parameters"]["columns"]
        values = timeseries_json["data"]["values"]

        if values is None:
            return None

        # Convert all timestamps to datetime objects
        for lst in values:
            new_datetime = datetime.strptime(lst[0], "%Y-%m-%dT%H:%M:%SZ")
            lst[0] = new_datetime

        return [dict(zip(columns, lst)) for lst in values]


    ################ ASSET/PROFILE/METRICS ################

    def get_asset_profile(self, asset_key):
        """Get all of the qualitative information for an asset.

        Args:
            asset_key (str): This "key" can be the asset's ID (unique), slug (unique), or symbol (non-unique)

        Returns:
            object: a python requests object
        """
        path = f"/api/v2/assets/{asset_key}/profile"
        return self._get(path, parameters=None)


    def extract_profile(self, profile_response):
        """Extracts very specific information from a coins profile

        Args:
            profile_response (str): Response from the Messari get profile method

        Returns:
            dict: flat dict
        """
        profile_json = profile_response.json()["data"]

        is_capped_supply =  profile_json["economics"]["consensus_and_emission"]["supply"]["is_capped_supply"]
        max_supply = profile_json["economics"]["consensus_and_emission"]["supply"]["max_supply"]

        genesis_block_date = profile_json["economics"]["launch"]["initial_distribution"]["genesis_block_date "]
        token_distribution_date = profile_json["economics"]["launch"]["initial_distribution"]["token_distribution_date"]

        profile_dict = {
            "is_capped_supply": is_capped_supply,
            "max_supply": max_supply,
            "genesis_block_date": genesis_block_date,
            "token_distribution_date": token_distribution_date
        }

        return profile_dict





    ###################################### PRIVATE ######################################
    def _get(self, path, parameters=None):

        full_url = f"{self.base_url}{path}"
        return self.session.get(full_url, params=parameters)
