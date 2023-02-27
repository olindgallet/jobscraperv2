# Author: Olin Gallet
# Date: 8/11/2022
#
# The AirtableAsObserver sets up an Airtable that will be updated
# as job data gets scraped.  
#
# The following keys need to be set up in the ~/.bashrc file:
# 1. AIRTABLE_BASE_KEY
# 2. AIRTABLE_TABLE - the table name to fill
# 3. AIRTABLE_API_KEY


from datetime import date
from airtable import Airtable  
from .observerinterface import ObserverInterface
from ..jobdata import JobData
import os
import time
from dotenv import load_dotenv, find_dotenv

class AirtableAsObserver(ObserverInterface):
    def __init__(self):
        load_dotenv(find_dotenv())
        if 'AIRTABLE_BASE_KEY' in os.environ and \
           'AIRTABLE_TABLE_NAME' in os.environ and \
           'AIRTABLE_API_KEY' in os.environ:
            base_key = os.environ['AIRTABLE_BASE_KEY']
            table_name = os.environ['AIRTABLE_TABLE_NAME']
            api_key = os.environ['AIRTABLE_API_KEY']
            self._airtable = Airtable(base_key, table_name, api_key)
        else:
            raise Exception('Could not create observer.  Verify environment variables and airtable status')

    async def notify(self, job_data:JobData):
        d8 = date.today().strftime('%m/%d/%y')
        data = {'job_company' : job_data.get_company(), 'job_title' : job_data.get_title(), 'job_description' : job_data.get_description(), 'job_link' : job_data.get_link(), 'post_date' : d8}
        self._airtable.insert(data)
        time.sleep(.2)
