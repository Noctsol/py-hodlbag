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


###################################### CONFIG ######################################
# Script configs
env = qi.ezload()
DEBUG = 1
CURRENT_TIME = hlp.timestamp()

# Database info
DB_CONN_STR = env.get("postgres_conn_str")

# Classes used
db = pg.Ezpostgres.from_connection_string(DB_CONN_STR)  # Database conn


###################################### FUNCTIONS ######################################




###################################### BODY ######################################

