"""
Author: Olin Gallet
Date: 12/27/2022

The Terminal is used to display helpful messages to the user. 
To be used indepently of scraping messages.
"""

from plumbum import colors
from typing import List

class Terminal:
    def __init__(self):
        pass
    
    @staticmethod
    def display_attempting_scrape(filename:str, position:str, location:str, engine:List[str], output:List[str]):
        """
        Displays message that the scrape is being attempted.

        :param filename: the filename of the configuration
        :type filename: str
        :param position: the job position to seek
        :type position: str
        :param engine: the search engines to use
        :type engine: str[]
        :param output: the output to use to display results
        :type output: str[] 
        """
        print(colors.orchid | f'[Preparing to scrape using configuration {filename}]')
        print(colors.yellow | '  Attempting scrape with the following parameters')
        print(colors.yellow | f'  Position: {position}')
        print(colors.yellow | f'  Location: {location}')
        print(colors.yellow | f'  Engine(s):  {engine}')
        print(colors.yellow | f'  Output(s):  {output}')

    @staticmethod
    def display_usage_help():
        """
        Displays usage help message and possible parameters for the Jobscraper. 
        """
        print(colors.orchid | '[Usage]')
        print(colors.blue | '  python3 jobscraperv2.py [configuration.json]')
        print(colors.yellow | '  jobscraper is used to scrape various jobs into a database.')
        print()
        print(colors.yellow | '  configuration.json - the name of the json file with the configuration')

    @staticmethod
    def display_website_error(url, message):
        """
        Display an error message for the given url.

        :param url: the url of the website
        :type url: str
        """
        print(colors.orchid | '[Error]')
        print(colors.blue | f'  {url}')
        print(colors.yellow | '  could not be scraped.  Additional info:')
        print(colors.yellow | f'  {message}')
        print()

    @staticmethod
    def display_parse_error(filename, message):
        """
        Display an error message that the configuration was unable to be parsed.

        :param filename: the filename of the configuration
        :type url: str
        :param message: the error message
        :type message: str 
        """
        print(colors.orchid | '[Error]')
        print(colors.blue | f'  {filename}')
        print(colors.yellow | '  could not be parsed.  Additional info:')
        print(colors.yellow | f'  {message}')

    @staticmethod
    def display_configuration_not_found_error(filename, message):
        """
        Display an error message that the given filename was not found.

        :param url: the url of the website
        :type url: str
        """
        print(colors.orchid | '[Error]')
        print(colors.blue | f'  {filename}')
        print(colors.yellow | '  was not found.  Additional info:')
        print(colors.yellow | f'  {message}')