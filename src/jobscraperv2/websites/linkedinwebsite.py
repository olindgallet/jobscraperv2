# coding=utf-8
# 
# Scrapes the LinkedIn site and gathers job information.
#
# Author: Luke Geel
# Date: 30 June 2024

from bs4 import BeautifulSoup
import requests
from .websiteinterface import WebsiteInterface
from playwright.async_api import Browser
from .jobdata import JobData
import time
import asyncio  # Import asyncio for asynchronous sleep


class LinkedInWebsite(WebsiteInterface):
    ARTIFICIAL_INTELLIGENCE_JOBS = '''https://www.linkedin.com/jobs/search/?currentJobId=3931916976&f_TPR=r604800&geoId=102380872&keywords=artificial%20intelligence&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true'''
    MACHINE_LEARNING_JOBS = '''https://www.linkedin.com/jobs/search/?currentJobId=3931916976&f_TPR=r604800&geoId=102380872&keywords=machine%20learning&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true'''
    REAL_ESTATE_JOBS = '''https://www.linkedin.com/jobs/search/?currentJobId=3931916976&f_TPR=r604800&geoId=102380872&keywords=real%20estate&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true'''



    def __init__(self, url):
        super().__init__(url)

    async def scrape(self, browser:Browser):
        page = await browser.new_page()
        page.set_default_navigation_timeout(super()._DEFAULT_TIMEOUT)
        page.set_default_timeout(super()._DEFAULT_TIMEOUT)
        await page.goto(super().get_url())

        # SVG element selector using the 'id' attribute
        svg_button_selector = '#close-small'

        # Wait for the SVG element to be available and then click it
        await page.wait_for_selector(svg_button_selector)  # Ensures the element is loaded
        await page.click(svg_button_selector)

        await page.screenshot(path='debug_screenshot4.png')
        time.sleep(2)
        time.sleep(2)

        # Loop to repeat the scroll action three times
        for _ in range(50):
            see_more_selector = 'button[aria-label="See more jobs"].infinite-scroller__show-more-button--visible'
            if await page.is_visible(see_more_selector):
                # Click the 'See more jobs' button if it is visible
                await page.click(see_more_selector)
                print("Clicked the 'See more jobs' button.")
                await asyncio.sleep(1)  # Wait for dynamic content to load
            else:
                await page.mouse.move(300, 400)  # Adjust coordinates to be within the scrollable panel
                await page.mouse.wheel(0, 25000)  # Scroll down
                await asyncio.sleep(1)  # Use asyncio.sleep instead of time.sleep in async functions

        await page.screenshot(path='debug_screenshot5.png')

        # Wait for the job listings to load
        await page.wait_for_selector('ul.jobs-search__results-list')

        # Select all job listing elements
        jobs = page.locator('ul.jobs-search__results-list > li')

        # Iterate through each job listing
        job_count = await jobs.count()
        for i in range(job_count):
            print("jobs.nth(i): ", jobs.nth(i))
            # Extract job title, company, and location for each listing
            job_title = await jobs.nth(i).locator('h3.base-search-card__title').inner_text()
            job_link = await jobs.nth(i).locator('a.base-card__full-link').get_attribute('href')
            job_company = await jobs.nth(i).locator('h4.base-search-card__subtitle a').inner_text()
            job_location = await jobs.nth(i).locator('span.job-search-card__location').inner_text()
            job_description = "job description"

            job_data = JobData(job_company, job_title, job_description, job_link, job_location)
            await super().notify(job_data)