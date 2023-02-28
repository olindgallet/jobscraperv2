# Author: Olin Gallet
# Date: 9/2/2023
from .websiteinterface import WebsiteInterface
from playwright.async_api import Browser
from .jobdata import JobData

class HitMarkerWebsite(WebsiteInterface):
    DATA_JOBS = 'https://hitmarker.net/jobs?keyword=data&remote=only'
    ANALYST_JOBS = 'https://hitmarker.net/jobs?keyword=analyst&remote=only'
    def __init__(self, url):
        super().__init__(url)

    async def scrape(self, browser:Browser):
        page = await browser.new_page()
        await page.goto(super().get_url(), timeout=0)
        joblist = page.locator('//a[contains(@href, "/jobs/")]')
        for i in range(await joblist.count() - 1):
            try:
                job_link = await joblist.nth(i).get_attribute('href')
                job_title = await joblist.nth(i).inner_text()
                job_company = job_link[job_link.rfind('/') + 1:job_link.find('-') - 1].capitalize()
                job_description = 'No description available.'
                subpage = await browser.new_page()
                await subpage.goto(job_link, timeout=0)
                job_description = subpage.locator('//div[contains(@class, "prose")]')
                job_description = await job_description.inner_text()
                job_description = job_description[:99999] + (job_description[99999:] and '...')
                await subpage.close()
                job_data = JobData(job_company, job_title, job_description, job_link)
                await super().notify(job_data)
            except Exception as ex:
                print(ex)
        await page.close()
    
        