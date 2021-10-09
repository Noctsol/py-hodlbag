"""
Owner: Kevin B
Contributors: N/A
Date Created: 20210917

Summary:
    Library used to pull historical snap shot data from coin market cap.

    - Will be useds to refresh data weekly
    - Allows you to basically just back up a bunch of historical data all at once as long as CMC still exists

"""



# From PyPi
from bs4 import BeautifulSoup       # For reading through all our html
from selenium import webdriver      # Controls browser
from selenium.webdriver.chrome.options import Options      # Modify Selenium config
import requests                     # Got sending the request to get the html from a webpage

# Default Installed
from pathlib import Path

import random                       # Randomizing numbers
import re                           # Regex for doing wildcard searches using beautiful soup
import calendar                     # Used for converting months to numbers
import datetime                     # Used to deal with datetime
import os                           # Windows systems control
import time                         # For sleeps
import sys                          # For exiting script if need be



class CoinMarketCapScrape:
    """ My wonderful class to siphon data off of CoinMarketCap cause I kind of hate them. """
    def __init__(self, brave_or_chrome_path=None):
        self.base_url = "https://coinmarketcap.com"
        self.historical_url = f"{self.base_url}/historical"

        # Selenium configs
        self.browser_path = brave_or_chrome_path if brave_or_chrome_path is not None else "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
        self.root_dir = Path(os.path.dirname(os.path.abspath(__file__))).parent

    ############################################################################### PUBLIC ###############################################################################

    ########### PRIMARY USER/APP FUNCTIONS ###########
    # If you're trying to use this, this is really all the stuff you should be interested in

    # Will get you a dictionary of all available snapshots times and their urls
    def get_available_historical_snapshots(self):
        ''' Returns dictionary of all available dates that are snapshotted on CMC '''

        # Stores all informatrion returned to user
        available_snapshots = {}

        # Getting all the available years
        year_soups = self.get_year_soups()

        # Mapping months to numbers
        month_map = self.__create_month_dict()

        # Cycling through each year
        for yr_soup in year_soups:
            # Getting the year displayed on the div
            year_text = self.extract_year_text(yr_soup)
            year_num = int(year_text)                           # Converting to int for later

            # Getting available months for this year
            month_soups = self.get_month_soups(yr_soup)

            # Cycling through each month within year
            for mt_soup in month_soups:

                # Getting the month displayed on the div
                month_text = self.extract_month_text(mt_soup)
                month_num = month_map[month_text]               # Mapping Month Name to Number

                # Getting available days within each month
                day_soups = self.get_day_soups(mt_soup)

                # Cycling through each day within the month
                for d_soup in day_soups:

                    # Extracting info
                    day_text = self.extract_day_text(d_soup)    # Getting day
                    day_num = int(day_text)
                    day_href =  self.extract_day_href(d_soup)   # Getting link to info about this day

                    # Generating info
                    snapshot_datetime = datetime.datetime(year_num, month_num, day_num)     # Actual datetime
                    str_datetime = snapshot_datetime.strftime("%Y-%m-%d")                   # Str datetime
                    link_to_snapshot = f"{self.base_url}{day_href}"

                    # Storing all info inside dict
                    snapshot_dict = {"date": str_datetime, "href": link_to_snapshot}

                    # Adding stored info to dict
                    available_snapshots[snapshot_datetime] = snapshot_dict

        return available_snapshots

    # Will get a snapshot data for 1 particular date
    def get_date_snapshot_data(self, url):
        ''' Returns snapshot data for a given data from CMC '''

    # TODO: Finish this function then use it in get all dates snapshot
    # def get_date_snapshots_data_range(self, from_date, to_date):
    #     from_datetime = datetime.datetime.strptime(from_date, "%Y-%m-%d")
    #     to_datetime = datetime.datetime.strptime(to_date, "%Y-%m-%d")
    #     available_snapshot_dates = self.get_available_historical_snapshots()
    #     for date_key in available_snapshot_dates:
    #         # Ignore any dates outside
    #         if from_datetime <= date_key or date_key =>
    #     pass

    # Pulls ALL historical data from the historical page - added a optional parameter to pull n amount of dates only
    def get_all_date_snapshots_data(self, n_dates_to_pull=0):
        ''' Returns a list of dictionaries containing all available snapshot data on CMC

            Params:
            - sleep - The amount of time we wait by default in between each request. Don't get IP banned bro.
            - n_dates_to_pull - Test feature to only pull n amount of dates to test the function
         '''

        # Will hold all results
        historical_data = []

        # Getting all available snapshot urls
        available_snapshot_dates = self.get_available_historical_snapshots()


        # Starting Selenium Session
        browser = self.create_browser_session()

        count = 0

        # Cycling through all snapshots amd getting data
        for date_key in available_snapshot_dates:
            # if date_key.year in [2013, 2014, 2015, 2016, 2017]:
            #     continue

            info = available_snapshot_dates[date_key]
            url = info["href"]
            datestamp = info["date"]

            print(f"Pulling historical data for {datestamp}")


            table_soup = self.get_table_soup_via_selenium(browser, url)

            # table_soup = self.get_table_soup(url)


            # header_soups = self.get_header_col_soups(table_soup)
            # headers = [i.text for i in header_soups]
            # print(headers)

            row_soups = self.get_row_soups(table_soup)

            for row_sp in row_soups:
                # print(row_sp)
                try:
                    row_dict = {
                        "date": datestamp,
                        "rank": self.extract_rank_text(row_sp),
                        "name": self.extract_name_text(row_sp),
                        "symbol": self.extract_symbol_text(row_sp),
                        "market_cap": self.extract_market_cap_text(row_sp),
                        "price": self.extract_price_text(row_sp),
                        "circulating_supply": self.extract_circulating_supply_text(row_sp),
                        "1h": self.extract_1h_text(row_sp),
                        "24h": self.extract_24h_text(row_sp),
                        "7d": self.extract_7d_text(row_sp)
                        }


                except Exception:
                    print(row_sp)
                    sys.exit()

                historical_data.append(row_dict)

            count+=1

            if count == n_dates_to_pull:
                break

            time.sleep(random.randint(3,9))

        browser.quit()


        return historical_data



    ########### HISTORICAL FRONTPAGE ELEMENT/DIV NAVIGATION ###########
    # Functions that parse through and navigate to the content we are interested in #

    # Pulls HTML for entire /historical/ page
    def get_historical_html(self):
        ''' Returns the source html for the historical snapshot dir '''
        return self.__get_html(self.historical_url)

    # Pulls the entire div that holds all time values pointing to snapshots
    def get_historical_data_soup(self):
        ''' Returns a bs soup object representing the historical snapshot dir '''
        html_content = self.get_historical_html()
        soup = BeautifulSoup(html_content, 'html.parser')

        # (1a) Getting the entire div that holds all time frames
        all_snapshots_soup = soup.find("div", {"class": "container cmc-main-section"})

        return all_snapshots_soup

    # Pulls all the html data for each year
    def get_year_soups(self):
        ''' Returns a bs soup object representing available data for a given year'''
        all_soup = self.get_historical_data_soup()
        year_snapshots_soups = all_soup.find_all("div", {"class": re.compile("eUVPSq")})
        return year_snapshots_soups

    # Pull all the available months for a given year_soup (singular!)
    def get_month_soups(self, year_soup):
        ''' Returns a bs soup object containing all the snapshotted months available for a year '''
        month_soups = year_soup.find_all("div", {"class": re.compile("jctIId")})
        return month_soups

    # Gets all the divs displaying day information within a month_soup
    def get_day_soups(self, month_soup):
        ''' Returns a bs soup object containing all the snapshotted days for a given year '''
        day_soups = month_soup.find_all("a", {"class": re.compile("historical-link cmc-link")})
        return day_soups

    ########### SELENIUM FUNCTION ###########

    # Create a selenium crhome browser session
    def create_browser_session(self):
        ''' Pops open a Selenium browser session '''
        driver_path = f"{self.root_dir}/ref/chromedriver.exe"
        driver = webdriver.Chrome(driver_path)
        driver.maximize_window()
        return driver


    # Scrolls all the way down a a page until theres nothing left - stack overflow credit
    def scroll_down(self, browser_session):
        ''' Will keep infinitely scrolling down until the Y position no longer changes '''
        scroll_wait_time = 1
        last_height = browser_session.execute_script("return document.body.scrollHeight")
        height_target = 1000

        while True:
            # # Scroll down to bottom INSTANTLY
            # browser_session.execute_script("window.scrollTo(0, document.body.scrollHeight);")\

            # Scroll down by chunks
            browser_session.execute_script("window.scrollTo(0, "+str(height_target)+")")
            height_target+=1000

            # Wait to load page
            time.sleep(scroll_wait_time)

            # Calculate new scroll height and compare with last scroll height
            new_height = browser_session.execute_script("return document.body.scrollHeight")

            print(new_height, last_height)

            if new_height == last_height:
                break
            last_height = new_height

        return True

    ########### SNAPSHOT DATA PAGE ELEMENT/DIV NAVIGATION ###########
    # Functions that parse through and navigate to the content we are interested in #

    # Pulls HTML for entire /historical/yyyymmdd page
    def get_date_snapshot_html(self, cmc_date_url):
        ''' Returns the html displaying the actual asset ranking for a given snapshot date '''
        return self.__get_html(cmc_date_url)

    # Gets the div representing the table holding all the data for a specific date using Selenium
    def get_table_soup_via_selenium(self, browser_session, cmc_date_url):
        ''' Returns a bs soup object cotaining all the html  for a given snapshot date using selenium'''
        # Use browser and goi to url and scroll down to force elements to load
        browser_session.get(cmc_date_url)
        self.scroll_down(browser_session)

        # Get html
        page_source =  browser_session.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        table_soup = soup.find_all("div", {"class": "cmc-table__table-wrapper-outer"})
        return table_soup[2]

    # Gets the div representing the table holding all the data for a specific date
    def get_table_soup(self, cmc_date_url):
        ''' Returns a bs soup object cotaining all the html  for a given snapshot date'''
        html_content = self.get_date_snapshot_html(cmc_date_url)
        soup = BeautifulSoup(html_content, 'html.parser')

        print("\n"*5)
        print(soup.encode('utf-8', 'ignore'))
        print("\n"*5)

        # Getting div holding all the rows for each asset/crypto
        # TODO: Not sure how to handle limitations with beautiful soup not being exact - find doesn't work because it automatically does a wild card
        table_soup = soup.find_all("div", {"class": "cmc-table__table-wrapper-outer"})

        # for i in table_soup:
        #     print("\n"*5)
        #     print(i)

        return table_soup[2]

    # Gets the divs representing the header columns
    def get_header_col_soups(self, table_soup):
        ''' Returns a bs soup object that returns all the header columns for a table holding snapshot data '''
        header_soup = table_soup.find("thead")
        header_col_soups = header_soup.find_all("th", {"class": re.compile("cmc-table__cell cmc-table__header")})
        return header_col_soups

    # Gets the divs representing the data rows
    def get_row_soups(self, table_soup):
        ''' Gets all the divs that hold all the row representing each asset
            I had to use a lambda function because bs4 does wildcard searches naturally and this
            ended up getting incorrect results. '''

        # Getting the starting point of the rows within the table
        body_soup = table_soup.find("tbody")

        # Getting all the row - read doc string for details
        row_soups =  body_soup.find_all(lambda tag: tag.name == 'tr' and tag.get('class') == ["cmc-table-row"])
        return row_soups


    ########### HISTORICAL FRONTPAGE EXTRACTION ###########
    # Functions that pull text information out of a given div #

    # Gets the span for a given year
    def extract_year_text(self, year_soup):
        ''' Returns the year of a snapshot date'''
        year_txt_div_soup = year_soup.find("div", {"class": re.compile("lgiEcX")})
        year_txt = year_txt_div_soup.text
        return year_txt

    # Finds and extract the text from div elementent displaying Month Name within a month_soup
    def extract_month_text(self, month_soup):
        ''' Returns the month of a snapshot date'''
        month_txt_div_soup = month_soup.find("div", {"class": re.compile("eSQiCH")})
        month_txt = month_txt_div_soup.text
        return month_txt

    # Extract text from the div element displaying the day of the month
    def extract_day_text(self, day_soup):
        ''' Returns the day of a snapshot date'''
        return day_soup.text

    # Extract href from the div element displaying the day of the month
    def extract_day_href(self, day_soup):
        ''' Returns the link to a snapshot date'''
        return day_soup["href"]


    ########### SNAPSHOT DATA PAGE EXTRACTION ###########
    # Functions that pull text information out of a given div #

    def extract_header_col_text(self, header_col_soup):
        ''' Get the actual text from a header column '''
        return header_col_soup.text

    # Gets the text from the element displaying the rank from the row soup
    def extract_rank_text(self, row_soup):
        ''' Get the actual rank text from a row holding information about a  coin/token '''
        col_soup = row_soup.find("td", {"class": re.compile("__rank")})
        return col_soup.text

    # Gets the text from the element displaying the name from the row soup
    def extract_name_text(self, row_soup):
        ''' Get the actual name text from a row holding information about a  coin/token '''
        actual_name_soup = row_soup.find("a", {"class": re.compile("--name")})
        return actual_name_soup.text

    # Gets the text from the element displaying the symbol from the row soup
    def extract_symbol_text(self, row_soup):
        ''' Get the actual symbol text from a row holding information about a  coin/token '''
        col_soup = row_soup.find("td", {"class": re.compile("__symbol")})
        return col_soup.text

    # Gets the text from the element displaying the market_cap from the row soup
    def extract_market_cap_text(self, row_soup):
        ''' Get the actual martket_cap text from a row holding information about a  coin/token '''
        col_soup = row_soup.find("td", {"class": re.compile("__market-cap" )})
        return self.__clean_money_value(col_soup.text)

    # Gets the text from the element displaying the price from the row soup
    def extract_price_text(self, row_soup):
        ''' Get the actual price text from a row holding information about a  coin/token '''
        col_soup = row_soup.find("td", {"class": re.compile("__price" )})
        return self.__clean_money_value(col_soup.text)

    # Gets the text from the element displaying the circulating supply from the row soup
    def extract_circulating_supply_text(self, row_soup):
        ''' Get the actual circulating supply text from a row holding information about a  coin/token '''
        col_soup = row_soup.find("td", {"class": re.compile("__circulating-supply" )})
        unformatted_supply = col_soup.text
        unneeded_index = unformatted_supply.index(" ")
        clean_supply = unformatted_supply[0:unneeded_index]
        return self.__clean_money_value(clean_supply)

    # Gets the text from the element displaying the %1h from the row soup
    def extract_1h_text(self, row_soup):
        ''' Get the actual 1h text from a row holding information about a  coin/token '''
        col_soup = row_soup.find("td", {"class": re.compile("__percent-change-1-h")})
        return self.__clean_percentage(col_soup.text)

    # Gets the text from the element displaying the %24h from the row soup
    def extract_24h_text(self, row_soup):
        ''' Get the actual 24h text from a row holding information about a  coin/token '''
        col_soup = row_soup.find("td", {"class": re.compile("__percent-change-24-h" )})
        return self.__clean_percentage(col_soup.text)

    # Gets the text from the element displaying the %7d from the row soup
    def extract_7d_text(self, row_soup):
        ''' Get the actual 7d text from a row holding information about a coin/token '''
        col_soup = row_soup.find("td", {"class": re.compile("__percent-change-7-d" )})
        return self.__clean_percentage(col_soup.text)


    ########### HELPER ###########


    ############################################################################### PRIVATE ###############################################################################

    ########### HELPER ###########

    # Pulls HTML content in as a string
    def __get_html(self, url):
        return requests.get(url).content

    # Generates a dictionary mapping full proper case month names to their respective numbers in the calendar year
    def __create_month_dict(self):
        month_dict = {}
        for item,i in enumerate(calendar.month_name):
            month_dict[i] = item

        return month_dict


    # Removes list of characters from a string
    def __strip_chars(self, chars_list, value):
        new_value = value
        for char in chars_list:
            new_value = new_value.replace(char, "")
        return new_value

    # Removes $ and commas from a string
    def __clean_money_value(self, value):
        return self.__strip_chars(["$", ","], value)

    # Removes % symbol
    def __clean_percentage(self, value):
        return value.replace("%", "")
