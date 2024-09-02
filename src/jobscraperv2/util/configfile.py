"""
Author: Olin Gallet
Date: 9/1/2024

The ConfigFile represents a configuration file for the scraper.
It provides utility to check the file and to read the file into an array.
Errors will be handled by the calling class.
"""

from os.path import exists
import json

class ConfigFile:
    
    def __init__(self, filename:str):
        """
        Initializes the configuration file.

        :param filename: the full filename of the configuration file
        :type filename: str 
        """
        self._filename = filename
    

    def exists(self):    
        """
        Checks if the given file exists.

        :return: `True` if the file exists, `False` if it does not
        :rtype: bool
        """ 
        return exists(self._filename)
    
    def parse(self):
        """
        Attempts to parse the configuration file.

        :raises Exception: if the configuration file is not found, the file is not valid JSON, or
        if it does not validate

        :return: an array of the configuration file.
        :rtype str[]
        """
        with open(self._filename) as file:
            json_file = json.load(file)
            if "position" not in json_file or \
               "location" not in json_file or \
               "engine" not in json_file or \
               "output" not in json_file:
                raise Exception("File format is invalid.")
        return json_file


    
