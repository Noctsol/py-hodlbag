"""
Owner: Kevin B
Contributors: N/A
Date Created: 20210824

Summary:
    This is tradition from all the people I've ever had the privilege of working with. Write lazy code. Why think when you can use helper?

"""

# Default Python Packages
import os                           # Deals with operating system functionality
import csv                          # For reading/writing csv files
import datetime                     # For dealing with datetime objs

class Helper():
    # Constructor - empty for this class
    def __init__(self) -> None:
        pass
    
    def read_csv(self):
        pass

    def write_to_csv(self, path, data, delimiter=","): 
        with open( path, 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f, delimiter=delimiter)

            # write multiple rows
            writer.writerows(data)

    def listdict_to_2dlist(self, list_of_dictionaries):

        headers = [key for key in list_of_dictionaries[0]]
        table = [headers]

        for dct in list_of_dictionaries:
            temp_lst = []
            for ikey in dct:
                temp_lst.append(dct[ikey])
            table.append(temp_lst)

        return table
    
    def timestamp(self):
        now = datetime.datetime.now()
        return now.strftime("%Y%m%d_%H%M%S")

    # Generates a directory only when it doesn't exist
    def mkdir(self, folder_path):
        # Only make directory if it doesn't exist
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
    
