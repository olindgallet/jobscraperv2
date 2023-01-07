# Author: Olin Gallet
# Date: 12/27/2022
#
# The Terminal is used to display helpful messages to the user. 
# To be used indepently of scraping messages.

from plumbum import colors

class Terminal:
    def __init__(self):
        pass
    
    @staticmethod
    def display_usage_help():
        """Displays usage help message and possible parameters for the Jobscraper.
        """
        print(colors.orchid | '[Usage]')
        print(colors.blue | '  python3 [-a] [-t] jobscraperv2.py')
        print(colors.yellow | '  jobscraper is used to scrape various jobs into a database.')
        print()
        print(colors.yellow | '  -a | send data to an Airtable defined in environment variabes')
        print(colors.yellow | '  -t | send data to the terminal')

    @staticmethod
    def display_website_error(url, message):
        """Display an error message for the given url.

        :param: url the url of the website
        :type: String
        """
        print(colors.orchid | '[Error]')
        print(colors.blue | url)
        print(colors.yellow | 'could not be scraped.  Additional info:')
        print(colors.yellow | message)
        print()