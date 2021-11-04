"""
Owner: Noctsol
Contributors: N/A
Date Created: 20210824

Summary:
    Helper methods for this

"""



# Default Python Packages
from datetime import datetime, timedelta

def calculate_interval_datetimes(timestamp=None, timeframe="1d", n_timeframes=2016):
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

def test_timeframes():
    """ I wrote this function to check calculate_timeframe_dates() because
    its kind of a complicated function and I needed to do sanity checks
    """

    n_times = 5
    test_datetime = datetime(2020, 12, 30)
    startend = calculate_interval_datetimes(timestamp=test_datetime,
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



