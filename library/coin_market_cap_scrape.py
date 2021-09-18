"""
Owner: Kevin B
Contributors: N/A
Date Created: 20210917

Summary:
    Library used to pull historical snap shots from coin market cap

"""



# From PyPi
from bs4 import BeautifulSoup       # For reading through all our html
import requests                     # Got sending the request to get the html from a webpage

# Default Installed
import re                           # Regex for doing wildcard searches using beautiful soup
import calendar                     # Used for converting months to numbers
import datetime                     # Used to deal with datetime



class CoinMarketCapScrape:
    def __init__(self):
        self.base_url = "https://coinmarketcap.com"
        self.historical_url = f"{self.base_url}/historical"

        # Properties specifying specific names of certain div elements on coinmarketcap
        self.historical_frame_class_name = "container cmc-main-section"
        self.years_box_class_name = "eUVPSq"
        self.month_box_class_name = "jctIId"
        self.day_box_class_name = "historical-link cmc-link"

        self.years_text_class_name = "lgiEcX"
        self.month_text_class_name = "eSQiCH"

    ############################################################################### PUBLIC ###############################################################################

    ########### Primary User/App Functions ###########
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


    ########### HISTORICAL FRONTPAGE ELEMENT/DIV NAVIGATION ###########
    # Functions that parse through and navigate to the content we are interested in 

    # Pulls HTML 
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


    ############################################################################### PRIVATE ###############################################################################

    # Pulls HTML content in as a string
    def __get_html(self, url):
        return requests.get(url).content

    # Generates a dictionary mapping full proper case month names to their respective numbers in the calendar year
    def __create_month_dict(self):
        month_dict = {}
        for n,i in enumerate(calendar.month_name):
            month_dict[i] = n

        return month_dict



