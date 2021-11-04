"""
Owner: Noctsol
Contributors: N/A
Date Created: 2021-10-30

Summary:
    FILL
"""


# Preinstalled packages
import os
import sys

# From Pypi
import helpu as hlp
import quikenv as qi

# From Project
from library import ezpostgres as pg



class EzMessari:
    """Class made to access Messari.io's API Client.
        You can initialize this class with/without an api key

    """
    def __init__(self, apikey=None):
        self.base_url = "https://data.messari.io"
        self.api_key = apikey
        self.someprop = "yo"


    ###################################### PUBLIC ######################################


    ###################################### PRIVATE ######################################






