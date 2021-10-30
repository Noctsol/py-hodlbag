"""
Owner: Noctsol
Contributors: N/A
Date Created: 20211011

Summary:
    For testing random helper library functions
"""

import sys
sys.path.append('.')

from library import helper
from datetime import datetime
import json


FILE_PATH ="./ref/cryptowatch_btc_historical.json"

hlp = helper.Helper()

with open(FILE_PATH, "r") as file:

    json_data = json.load(file)

    for i in json_data["result"]["86400"]:
        ts = int(i[0])

        datestamp = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

        if datestamp == "2021-10-11 00:00:00":
            print(i)
