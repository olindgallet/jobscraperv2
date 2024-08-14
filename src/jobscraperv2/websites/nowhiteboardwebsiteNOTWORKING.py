# Author: Olin Gallet
# Date: 28/2/2023
from .websiteinterface import WebsiteInterface
from playwright.async_api import Browser
from .jobdata import JobData

class NoWhiteboardWebsite(WebsiteInterface):
    DATA_JOBS = 'https://www.nowhiteboard.org/?&page=1&search=data&location=Remote%20(United%20States)'
    
    _BASE_URL = 'https://www.nowhiteboard.org'
    
    def __init__(self, url):
        super().__init__(url)

    async def scrape(self, browser:Browser):
        page = await browser.new_page()
        await page.goto(super().get_url(), timeout=0)
        joblist = page.locator('div[class="job-container"]')
        for i in range(0, await joblist.count() - 1):
            try:
                job_company = await joblist.nth(i).locator('div[class="company"]').locator('a').inner_text()
                job_title = await joblist.nth(i).locator('xpath=div/div/div/a').inner_text()
                job_link = await joblist.nth(i).locator('xpath=div/div/div/a').get_attribute('href')
                job_link = self._BASE_URL + job_link

                subpage = await browser.new_page()
                subpage.set_default_navigation_timeout(super()._DEFAULT_TIMEOUT)
                subpage.set_default_timeout(super()._DEFAULT_TIMEOUT)
                await subpage.goto(job_link, timeout=0)

                job_description = subpage.locator('div[class="job-description"]')
                job_description = await job_description.inner_text()
                job_description = job_description[:99999] + (job_description[99999:] and '...')
                await subpage.close()

                job_data = JobData(job_company, job_title, job_description, job_link)
                await super().notify(job_data)

            except Exception as ex:
                print(ex)
        await page.close()
    
        