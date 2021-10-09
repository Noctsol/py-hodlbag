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
import requests                     # Got sending the request to get the html from a webpage

# Default Installed
import re                           # Regex for doing wildcard searches using beautiful soup
import calendar                     # Used for converting months to numbers
import datetime                     # Used to deal with datetime
import time
import sys



class CoinMarketCapScrape:
    def __init__(self):
        self.base_url = "https://coinmarketcap.com"
        self.historical_url = f"{self.base_url}/historical"

        # Properties specifying specific names of certain div elements on coinmarketcap historicalfront page (* indicates wildcard search)
        self.historical_frame_class_name = "container cmc-main-section"
        self.years_box_class_name = "eUVPSq"                                    # *
        self.month_box_class_name = "jctIId"                                    # *
        self.day_box_class_name = "historical-link cmc-link"    
        self.years_text_class_name = "lgiEcX"                                   # *
        self.month_text_class_name = "eSQiCH"                                   # *

        # Properties specifying specific names of certain div elements on coinmarketcap snapshot page (* indicates wildcard search)
        self.data_table_class_name = "cmc-table__table-wrapper-outer"
        self.data_headers_obj = "thead"
        self.data_headers_col_class_name = "cmc-table__cell cmc-table__header"  # *
        self.data_row_obj = "tbody"
        self.data_row_class_name = "cmc-table-row"
        self.data_row_col_class_name = "cmc-table__cell cmc-table__cell"        # *

        self.data_rank_class_name = "__rank"                                    # *
        self.data_name_class_name = "__name"                                    # *
        self.data_name2_class_name = "--name"                                   # *
        self.data_symbol_class_name = "__symbol"                                # *
        self.data_cap_class_name = "__market-cap"                               # *
        self.data_price_class_name = "__price"                                  # *
        self.data_supply_class_name = "__circulating-supply"                    # *
        self.data_1h_class_name = "__percent-change-1-h"                        # *
        self.data_24h_class_name = "__percent-change-24-h"                      # *
        self.data_7d_class_name = "__percent-change-7-d"                        # *

    ############################################################################### PUBLIC ###############################################################################

    ########### PRIMARY USER/APP FUNCTIONS ###########
    # If you're trying to use this, this is really all the stuff you should be interested in

    # Will get you a list of all available snapshots times and their urls
    def get_available_historical_snapshots(self):

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

    def get_date_snapshot_data(self, url):
        pass

    # def get_date_snapshots_data_range(self, from_date, to_date):
    #     from_datetime = datetime.datetime.strptime(from_date, "%Y-%m-%d")
    #     to_datetime = datetime.datetime.strptime(to_date, "%Y-%m-%d")
    #     available_snapshot_dates = self.get_available_historical_snapshots()
    #     for date_key in available_snapshot_dates:
    #         # Ignore any dates outside 
    #         if from_datetime <= date_key or date_key =>
    #     pass

    # Pulls ALL historical data from the historical page - added a optional parameter to pull n amount of dates only
    def get_all_date_snapshots_data(self, sleep=2, n_dates_to_pull=0):

        # Will hold all results
        historical_data = []

        # Getting all available snapshot urls
        available_snapshot_dates = self.get_available_historical_snapshots()

        n = 0

        # Cycling through all snapshots amd getting data
        for date_key in available_snapshot_dates:
            info = available_snapshot_dates[date_key]
            url = info["href"]
            datestamp = info["date"]

            print(f"Pulling historical data for {datestamp}")

            table_soup = self.get_table_soup(url)

            # header_soups = self.get_header_col_soups(table_soup)
            # headers = [i.text for i in header_soups]
            # print(headers)

            row_soups = self.get_row_soups(table_soup)
            for row_sp in row_soups:
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
                    print(row_dict)
                    sys.exit()

                historical_data.append(row_dict)
            
            n+=1

            if n == n_dates_to_pull:
                break

            time.sleep(sleep)
            

        return historical_data

            


    ########### HISTORICAL FRONTPAGE ELEMENT/DIV NAVIGATION ###########
    # Functions that parse through and navigate to the content we are interested in #
    
    # Pulls HTML for entire /historical/ page
    def get_historical_html(self):
        return self.__get_html(self.historical_url)

    # Pulls the entire div that holds all time values pointing to snapshots
    def get_historical_data_soup(self):
        html_content = self.get_historical_html()
        soup = BeautifulSoup(html_content, 'html.parser')

        # (1a) Getting the entire div that holds all time frames
        all_snapshots_soup = soup.find("div", {"class": self.historical_frame_class_name})

        return all_snapshots_soup
    
    # Pulls all the html data for each year
    def get_year_soups(self):
        all_soup = self.get_historical_data_soup()
        year_snapshots_soups = all_soup.find_all("div", {"class": re.compile(self.years_box_class_name)})
        return year_snapshots_soups

    # Pull all the available months for a given year_soup (singular!)
    def get_month_soups(self, year_soup):
        month_soups = year_soup.find_all("div", {"class": re.compile(self.month_box_class_name)})
        return month_soups

    # Gets all the divs displaying day information within a month_soup
    def get_day_soups(self, month_soup):
        day_soups = month_soup.find_all("a", {"class": re.compile(self.day_box_class_name)})
        return day_soups


    ########### SNAPSHOT DATA PAGE ELEMENT/DIV NAVIGATION ###########
    # Functions that parse through and navigate to the content we are interested in #

    # Pulls HTML for entire /historical/yyyymmdd page
    def get_date_snapshot_html(self, cmc_date_url):
        return self.__get_html(cmc_date_url)

    # Gets the div representing the table holding all the data for a specific date
    def get_table_soup(self, cmc_date_url):
        html_content = self.get_date_snapshot_html(cmc_date_url)
        soup = BeautifulSoup(html_content, 'html.parser')

        # Getting div holding all the rows for each asset/crypto
        # TODO: Not sure how to handle limitations with beautiful soup not being exact - find doesn't work because it automatically does a wild card
        table_soup = soup.find_all("div", {"class": self.data_table_class_name})[2]
        return table_soup
        
    # Gets the divs representing the header columns
    def get_header_col_soups(self, table_soup):
        header_soup = table_soup.find(self.data_headers_obj)
        header_col_soups = header_soup.find_all("th", {"class": re.compile(self.data_headers_col_class_name)})
        return header_col_soups
    
    # Gets the divs representing the data rows
    def get_row_soups(self, table_soup):
        body_soup = table_soup.find(self.data_row_obj)
        row_soups =  body_soup.find_all("tr", {"class": self.data_row_class_name})
        return row_soups
    

    ########### HISTORICAL FRONTPAGE EXTRACTION ###########
    # Functions that pull text information out of a given div #

    # Gets the span for a given year
    def extract_year_text(self, year_soup):
        year_txt_div_soup = year_soup.find("div", {"class": re.compile(self.years_text_class_name)})
        year_txt = year_txt_div_soup.text
        return year_txt

    # Finds and extract the text from div elementent displaying Month Name within a month_soup
    def extract_month_text(self, month_soup):
        month_txt_div_soup = month_soup.find("div", {"class": re.compile(self.month_text_class_name)})
        month_txt = month_txt_div_soup.text
        return month_txt

    # Extract text from the div element displaying the day of the month
    def extract_day_text(self, day_soup):
        return day_soup.text

    # Extract href from the div element displaying the day of the month
    def extract_day_href(self, day_soup):
        return day_soup["href"]


    ########### SNAPSHOT DATA PAGE EXTRACTION ###########
    # Functions that pull text information out of a given div #

    def extract_header_col_text(self, header_col_soup):
        return header_col_soup.text
    
    # Gets the text from the element displaying the rank from the row soup
    def extract_rank_text(self, row_soup):
        col_soup = row_soup.find("td", {"class": re.compile(self.data_rank_class_name)})
        return col_soup.text
    
    # Gets the text from the element displaying the name from the row soup
    def extract_name_text(self, row_soup):
        col_soup = row_soup.find("td", {"class": re.compile(self.data_name_class_name)})
        actual_name_soup = row_soup.find("a", {"class": re.compile(self.data_name2_class_name)})
        return actual_name_soup.text
    
    # Gets the text from the element displaying the symbol from the row soup
    def extract_symbol_text(self, row_soup):
        col_soup = row_soup.find("td", {"class": re.compile(self.data_symbol_class_name)})
        return col_soup.text

    # Gets the text from the element displaying the market_cap from the row soup
    def extract_market_cap_text(self, row_soup):
        col_soup = row_soup.find("td", {"class": re.compile(self.data_cap_class_name)})
        return self.__clean_money_value(col_soup.text)

    # Gets the text from the element displaying the price from the row soup
    def extract_price_text(self, row_soup):
        col_soup = row_soup.find("td", {"class": re.compile(self.data_price_class_name)})
        return self.__clean_money_value(col_soup.text)

    # Gets the text from the element displaying the circulating supply from the row soup
    def extract_circulating_supply_text(self, row_soup):
        col_soup = row_soup.find("td", {"class": re.compile(self.data_supply_class_name)})
        unformatted_supply = col_soup.text
        unneeded_index = unformatted_supply.index(" ")
        clean_supply = unformatted_supply[0:unneeded_index]
        return self.__clean_money_value(clean_supply)

    # Gets the text from the element displaying the %1h from the row soup
    def extract_1h_text(self, row_soup):
        col_soup = row_soup.find("td", {"class": re.compile(self.data_1h_class_name)})
        return self.__clean_percentage(col_soup.text)

    # Gets the text from the element displaying the %24h from the row soup
    def extract_24h_text(self, row_soup):
        col_soup = row_soup.find("td", {"class": re.compile(self.data_24h_class_name)})
        return self.__clean_percentage(col_soup.text)

    # Gets the text from the element displaying the %7d from the row soup
    def extract_7d_text(self, row_soup):
        col_soup = row_soup.find("td", {"class": re.compile(self.data_7d_class_name)})
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
        for n,i in enumerate(calendar.month_name):
            month_dict[i] = n

        return month_dict


    # Removes list of characters from a string
    def __strip_chars(self, chars_list, value):
        new_value = value
        for c in chars_list:
            new_value = new_value.replace(c, "")
        return new_value

    # Removes $ and commas from a string
    def __clean_money_value(self, value):
        return self.__strip_chars(["$", ","], value)

    # Removes % symbol
    def __clean_percentage(self, value):
        return value.replace("%", "")