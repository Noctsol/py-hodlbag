"""
Owner: Kevin B
Contributors: N/A
Date Created: 20211008

Summary:
    Testing script for Selenium

"""

import sys
sys.path.append('.')
from library import coin_market_cap_scrape as cmcs
from library import helper

from selenium import webdriver      # Controls browser
# Default Installed
from pathlib import Path
import os

scrape = cmcs.CoinMarketCapScrape()
hlp = helper.Helper()
root_dir = Path(os.path.dirname(os.path.abspath(__file__))).parent

driver_path = f"{root_dir}/ref/chromedriver.exe"
driver = webdriver.Chrome(driver_path)

driver.maximize_window()

driver.close()

driver = webdriver.Chrome(driver_path)

driver.get("https://stackoverflow.com/questions/15067107/difference-between-webdriver-dispose-close-and-quit")

# print(hlp.listdict_to_2dlist(data))
