# coding=utf-8
# 
# Scrapes the WeWorkRemotely site and gathers job information.
#
# Author: Olin Gallet
# Date: 25 Oct 2020
from bs4 import BeautifulSoup
import requests
from .websiteinterface import WebsiteInterface
from playwright.async_api import Browser
from .jobdata import JobData

class WeWorkRemotelyWebsite(WebsiteInterface):
    DATA_JOBS = 'https://weworkremotely.com/remote-jobs/search?term=data&button='
    #BACK_END_PROGRAMMING_JOBS = 'https://weworkremotely.com/categories/remote-back-end-programming-jobs'
    #FRONT_END_PROGRAMMING_JOBS = 'https://weworkremotely.com/categories/remote-front-end-programming-jobs'
    #FULL_STACK_PROGRAMMING_JOBS = 'https://weworkremotely.com/categories/remote-full-stack-programming-jobs'
    #SYS_ADMIN_JOBS = 'https://weworkremotely.com/categories/remote-devops-sysadmin-jobs'
    #PRODUCT_JOBS = 'https://weworkremotely.com/categories/remote-product-jobs'
    #CUSTOMER_SUPPORT_JOBS = 'https://weworkremotely.com/categories/remote-customer-support-jobs'

    def __init__(self, url):
        super().__init__(url)

    async def scrape(self, browser:Browser):
        resp = requests.get(super().get_url())
        soup = BeautifulSoup(resp.text, 'html.parser')
        links = soup.findAll('a')
        for link in links:
            if link.get('href') and '/remote-jobs/' in link.get('href') and not link.get('href').endswith('new') and not link.get('href').endswith('search'):
                job_title = link.find('span', {'class': 'title'}).text
                job_company = link.find('span', {'class': 'region company'}).text + ' @ ' + link.find('span', {'class': 'company'}).text
                job_link = 'https://weworkremotely.com' + link.get('href')

                job_subpage = requests.get(job_link)
                subpage_soup = BeautifulSoup(job_subpage.text, 'html.parser')
                subpage_listing = subpage_soup.find('div',{'id':'job-listing-show-container'})
                job_description = subpage_listing.text[:99999] + (subpage_listing.text[99999:] and '...')
                
                job_data = JobData(job_company, job_title, job_description, job_link)
                await super().notify(job_data)
        resp.close()
