# Author: Olin Gallet
# Date: 28/2/2023
from .websiteinterface import WebsiteInterface
from playwright.async_api import Browser
from .jobdata import JobData

class HimalayasWebsite(WebsiteInterface):
    DATA_ANALYST_JOBS = 'https://himalayas.app/jobs/data-analyst'
    DATA_SCIENTIST_JOBS = 'https://himalayas.app/jobs/data-scientist'
    BUSINESS_ANALYST_JOBS = 'https://himalayas.app/jobs/business-analyst'
    DATA_ENGINEER_JOBS = 'https://himalayas.app/jobs/data-engineer'
    ANALYTICS_JOBS = 'https://himalayas.app/jobs/analytics'

    _BASE_URL = 'https://himalayas.app'

    def __init__(self, url):
        super().__init__(url)

    async def scrape(self, browser:Browser):
        page = await browser.new_page()
        await page.goto(super().get_url(), timeout=0)
        joblist = page.locator('div[name="card"]')
        
        for i in range(0, await joblist.count() - 1):
            try:
                job_title = await joblist.nth(i).locator('xpath=div/div/div/a/h2').inner_text()
                job_link = await joblist.nth(i).locator('xpath=div/div/div/a').nth(0).get_attribute('href')
                job_link = self._BASE_URL + job_link
                job_company = await joblist.nth(i).locator('xpath=div/div/div/div/a/h3').inner_text()
                
                subpage = await browser.new_page()
                subpage.set_default_navigation_timeout(super()._DEFAULT_TIMEOUT)
                subpage.set_default_timeout(super()._DEFAULT_TIMEOUT)
                await subpage.goto(job_link, timeout=0)

                job_description = subpage.locator('main').nth(0)
                job_description = await job_description.inner_text()
                job_description = job_description[:99999] + (job_description[99999:] and '...')
                await subpage.close()

                job_data = JobData(job_company, job_title, job_description, job_link)
                await super().notify(job_data)
            except Exception as ex:
                print(ex)    
            i = i + 1
        await page.close()
    
        