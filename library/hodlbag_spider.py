"""
Owner: Noctsol
Contributors: N/A
Date Created: 2021-11-06

Summary:
    This class contains all the of the function that I have to use to manipulate data to gather it
"""


# Preinstalled packages
from datetime import datetime,timedelta
import math
import time

# From Pypi

# From Project
from . import ezmessari



class HodlbagSpider:
    """This class contains all the of the function that I have to use to manipulate data to gather it

        - Dealing with timeseries and calculatime the correct dates/dateimes
        - Calling API

    """
    def __init__(self, api_key):
        self.messari_client = ezmessari.EzMessari(api_key)
    ###################################### PUBLIC ######################################

    def datetime_to_datestring(self,my_datetime):
        """Convert a datetime to a date string in YYYY-MM-dd format"""
        return my_datetime.strftime("%Y-%m-%d")

    def yesterday(self):
        """Gets the UTC datetime 24 hours ago"""
        return datetime.utcnow() - timedelta(days=1)

    def calculate_interval_datetimes(self, timestamp=None, timeframe="1d", n_timeframes=2016):
        """Every API generally has a max alloted amount of data you can retrieve on timeseries
            calls per call. This function starts from given timestamp and looks back
            2010 "timeframes" for what that beginning datetime would be. 2016
            - Example: Starting at 2021-01-01 00:00:00 and looking back

            - Messari will return at max 2016 data points for any time frame

        Args:
            timestamp (datetime, optional): This date will be used to look back 2016- timeframes
                if filled out. Defaults to None.
            timeframe (str, optional): ["5m", "15m", "30m", "1h", "1d", "1w"] for 5 minute, 15 minute, 30 minute.
                1 hour, 1 day, and 1 week respectively . Defaults to "1d".
            n_timeframes (int, optional): Defaults to "2016" because messari allows about 2016 data points.

        Returns:
            tuple: tuple with the first and last date that you can retrieve for a given time frame
        """


        if timeframe not in ["5m", "15m", "30m", "1h", "4h", "12h","1d", "1w"]:
            raise ValueError('timeframe value must be in["5m", "15m", "30m", "1h", "1d", "1w"] ')

        end_time = datetime.utcnow()
        if timestamp is not None:
            end_time = timestamp

        # Lookback 2000 timeframes
        if timeframe == "5m":
            start_time = end_time - timedelta(minutes=n_timeframes*5)
        elif timeframe == "15m":
            start_time = end_time - timedelta(minutes=n_timeframes*15)
        elif timeframe == "30m":
            start_time = end_time - timedelta(minutes=n_timeframes*30)
        elif timeframe == "1h":
            start_time = end_time - timedelta(hours=n_timeframes*1)
        elif timeframe == "4h":
            start_time = end_time - timedelta(hours=n_timeframes*4)
        elif timeframe == "12h":
            start_time = end_time - timedelta(hours=n_timeframes*12)
        elif timeframe == "1d":
            start_time = end_time - timedelta(days=n_timeframes*1)
        elif timeframe == "1w":
            start_time = end_time - timedelta(hours=n_timeframes*7)

        return (start_time, end_time)

    def test_timeframes(self):
        """ I wrote this function to check calculate_timeframe_dates() because
        its kind of a complicated function and I needed to do sanity checks
        """

        n_times = 5
        test_datetime = datetime(2020, 12, 30)
        startend = self.calculate_interval_datetimes(timestamp=test_datetime,
                                            timeframe="1d",
                                            n_timeframes=5)

        # Calculating backwards
        b_end = startend[1]
        b_start = b_end
        for _ in range(n_times):
            b_start = b_start - timedelta(days=1)

        # Calculating forward
        f_start = startend[0]
        f_end = f_start

        for _ in range(n_times):
            f_end = f_end + timedelta(days=1)

        # Print for human understanding
        print(startend[0], startend[1])
        print(b_start, b_end)
        print(f_start, f_end, "\n")

        # Throw errors if none of this makes sense
        if not startend[0]==b_start==f_start:
            raise ArithmeticError("Starts times to not match")
        elif not startend[1]==b_end==f_end:
            raise ArithmeticError("End times do not match")

        return 1

    ################### MESSARI ###################

    def messari_intervals_to_2009(self):
        """Return an int that tells me how many calls I need to
        make to look back to 2009-01-01 as this is when, bitcoin,
        the first cryptocurrency was created. This makes the earliest
        possible historical data that could exist
        """
        # This script pulls things in days
        # If you want minute data, give me money and problem solved!~!
        days = (datetime.utcnow() - datetime(2009, 1, 1)).days

        # We use 2016 because this is the max rows messari allows per time interval
        calls_required = math.ceil(days/2016)

        return calls_required

    def calculate_all_messari_intervals(self):
        """Calculates all the amount of times we need to look back 2016 days
        to get back to 2009-01-01(when it all began)
        """
        n_messari_calls = self.messari_intervals_to_2009()
        interval_strings = []

        # Get yesterdays datetime (24h ago)
        lookback_time = self.yesterday()

        # Calculate time ranges of 2010 days to get back to 2009-01-01
        for _ in range(n_messari_calls):

            # Lookback for next time inv
            new_times = self.calculate_interval_datetimes(timestamp=lookback_time)

            # Convert datetime to strings
            interval_tuple = (self.datetime_to_datestring(new_times[0]), self.datetime_to_datestring(new_times[1]))
            interval_strings.append(interval_tuple)

            # Set new time to look back(minus 1 day to avoid duplicate data)
            lookback_time = new_times[0] - timedelta(days=1)

        return interval_strings

    def backfill_messari_timeseries(self, crypto_name, messari_metric_id, time_intervals):
        """Gets all the price OHLCV data for a crytocurrency on messari.io"""

        messari_timeseries_data = []

        n_intervals = len(time_intervals)
        counter = 0

        # Executing all api calls and extracting info
        while counter < n_intervals:

            start_time = time_intervals[counter][0]
            end_time = time_intervals[counter][1]
            # Making api call
            response = self.messari_client.get_asset_timeseries(crypto_name, messari_metric_id, start_time, end_time)

            if response.status_code == 429:
                print(response.status_code, response.json())
                time.sleep(60)
                continue
            elif response.status_code not in (200, 429):
                # Throw exception here
                print(response.status_code, response.json())
                raise Exception("API errored out")

            # Converting data to a flat dictionary
            flat_dict = self.messari_client.extract_timeseries(response)
            # This means messari has no data on this item
            if flat_dict is None:
                counter+=1
                continue

            # Add data to container
            messari_timeseries_data+=self.messari_client.extract_timeseries(response)

            counter+=1

        return messari_timeseries_data

    def get_messari_profile(self, asset_key):
        """Makes a call to the messari get profile api
            and returns formatted data

        """

        max_attempts = 3
        data = None

        for _ in range(max_attempts):
            # Make api call
            response = self.messari_client.get_asset_profile(asset_key)
            print(response.status_code, response.json())
            # Error handling API calls
            if response.status_code == 429:
                print(response.status_code, response.json())
                time.sleep(60)
                continue
            elif response.status_code == 404:
                break
            elif response.status_code not in (200, 429):
                # Throw exception here
                print(response.status_code, response.json())
                raise Exception("API errored out")

            data = self.messari_client.extract_profile(response)
            break


        return data
    ###################################### PRIVATE ######################################

