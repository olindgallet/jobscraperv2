# Author: Olin Gallet
# Date: 5/11/2022
#
# The WebsiteInterface is to be implemented by all potential websites
# that would be crawled.  It provides an abstract function for scraping the website.

from abc import ABC, abstractmethod
from playwright.async_api import async_playwright, Browser
from .observers.observerinterface import ObserverInterface
from .jobdata import JobData

class WebsiteInterface(ABC):
    #60 second default timeout
    _DEFAULT_TIMEOUT = 60000

    def __init__(self, url):
        self._observers = []
        self._url = url

    @abstractmethod
    async def scrape(self, browser:Browser):
        pass

    def get_url(self):
        return self._url

    def subscribe (self, observer:ObserverInterface):
        ''' Subscribes the given observer for notifications for jobs found on this site.
        :param: observer the observer to notify
        :type: ObserverInterface
        '''
        self._observers.append(observer)

    async def notify (self, job_data:JobData):
        ''' Notify all observers with provided job data
        :param: job_data the job data
        :type: JobData
        '''
        for observer in self._observers:
            await observer.notify(job_data)