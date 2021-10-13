"""
Owner: Kevin B
Contributors: N/A
Date Created: 20210824

Summary:
    This is tradition from all the people I've ever had the privilege of working with. Write lazy code. Why think when you can use helper?

"""



# Default Python Packages
from uuid import uuid4

import os                           # Deals with operating system functionality
import csv                          # For reading/writing csv files
import datetime                     # For dealing with datetime objs




class Helper():
    '''
    Helper class containing functions that are used a lot accross multiple projects.
    The intention here to to make some tedious things brain dead.
    '''

    # Read a csv file
    def read_csv(self, file_path, delimiter=",", quotechar='"'):
        ''' Read a csv file and returns a nested list with the header/data

        Parameters
        ----------
        file_path : string
            Absolute path of the file. Example:"C:/Users/Noctsol/Documents/somefile.csv"
        delimiter : string : default value = ","
            Delimiter of the the csv file. Default is a comma.
        quotechar : string : default value = '"'
            character use to enclose values. Default is quotations.
        '''

        with open(file_path, newline='') as csvfile:
            lsts = []
            csv_data = csv.reader(csvfile, delimiter=delimiter, quotechar=quotechar)
            for row in csv_data:
                lsts.append(row)

            return lsts

    # Outputs a 2d list to a csv file
    def write_to_csv(self, file_path, data, delimiter=","):
        ''' Writes a nested list to a csv file

        Parameters
        ----------
        file_path : string
            Absolute path of the file. Example:"C:/Users/Noctsol/Documents/somefile.csv"
        data : <list<list>>
            Nested list of data. Example: [["header1", "header2"], ["val1", "val2"]]
        delimiter : string : default value = ","
            Delimiter of the the csv file. Default is a comma.
        '''
        with open(file_path, 'w', encoding='UTF8', newline='') as file:
            writer = csv.writer(file, delimiter=delimiter)

            # write multiple rows
            writer.writerows(data)

            return True

    # Converts a list of dictionaries to a nested 2dlist
    def listdict_to_2dlist(self, list_of_dictionaries):
        ''' Converts a list of dictionaries to a nested 2dlist and return it

        Parameters
        ----------
        list_of_dictionaries : <list<dictionary>>
            A list of dictionary. Example: [{"key1": "val1"}, {"key2": "val2"}]

        '''

        # Get headers
        headers = [key for key in list_of_dictionaries[0]]
        table = [headers]   # append headers

        # Get data
        for dct in list_of_dictionaries:
            # Store values in temporary list
            temp_lst = []

            # Fetch values inside dictionary
            for ikey in dct:
                temp_lst.append(dct[ikey])

            # Add tempt list to table container
            table.append(temp_lst)

        return table

    # Generate a string datetime to use to write files
    def datetime_timestamp(self, formatting="%Y%m%d_%H%M%S" ):
        ''' Returns a string indicate a current datetime(Ex. 20150106_012259)

        Parameters
        ----------
        formatting : string : default value = "%Y%m%d_%H%M%S"
            Sets the format of datetime stamp that is returned.

        '''
        now = datetime.datetime.now()
        return now.strftime(formatting)

    # Generates a directory only when it doesn't exist
    def mkdir(self, folder_path):
        ''' Creates a directory ONLY when it doesn't exist

        Parameters
        ----------
        folder_path : string
            Indicates where new folder will be created (Ex. C:/Users/you/Documents/Repository)

        '''
        # Only make directory if it doesn't exist
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        return True

    # G enera
    def make_uuid(self):
        '''Generates a universally unique identifier (UUID) string
        (Example: 'f50ec0b7-f960-400d-91f0-c42a6d44e3d0')

        Parameters
        ----------
        None

        '''
        return str(uuid4())
