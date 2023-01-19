# Author: Olin Gallet
# Date: 18/1/2023
from .websiteinterface import WebsiteInterface
from playwright.async_api import Browser
from .jobdata import JobData

class Jobs4GoodWebsite(WebsiteInterface):
    GRETNA_JOBS = "https://www.learn4good.com/jobs/9764/gretna/la-louisiana/area/"
    HARVEY_JOBS = "https://www.learn4good.com/jobs/9769/harvey/la-louisiana/area/"
    MARRERO_JOBS = "https://www.learn4good.com/jobs/9777/marrero/la-louisiana/area/"
    NEW_ORLEANS_JOBS = "https://www.learn4good.com/jobs/9787/new-orleans/la-louisiana/area/"
    WESTWEGO_JOBS = "https://www.learn4good.com/jobs/9741/westwego/la-louisiana/area/"

    def __init__(self, url):
        super().__init__(url)

    async def scrape(self, browser:Browser):
        page = await browser.new_page()
        page.set_default_navigation_timeout(super()._DEFAULT_TIMEOUT)
        page.set_default_timeout(super()._DEFAULT_TIMEOUT)
        await page.goto(super().get_url())
        jobpages = page.locator('div[class="pagination"]').locator('a')
        job_location = 'No Location Found'
        
        if 'gretna' in super().get_url():
            job_location = 'Gretna'
        elif 'harvey' in super().get_url():
            job_location = 'Harvey'
        elif 'marrero' in super().get_url():
            job_location = 'Marrero'
        elif 'new-orleans' in super().get_url():
            job_location = 'New Orleans'
        elif 'westwego' in super().get_url():
            job_location = 'Westwego'
        
            
        for j in range(await jobpages.count() - 2):
            joblist = page.locator('table#main_job_list').locator('tr')
            for i in range(await joblist.count() - 1):
                try:
                    job_link = await joblist.nth(i).locator('a[class="job_title"]').get_attribute('href')
                    job_title = await joblist.nth(i).locator('a[class="job_title"]').inner_text()
                    job_company = await joblist.nth(i).locator('span[class="absent_link"]').inner_text() + ' @ ' + job_location
                    job_description = 'No description available.'
                    subpage = await browser.new_page()
                    subpage.set_default_navigation_timeout(super()._DEFAULT_TIMEOUT)
                    subpage.set_default_timeout(super()._DEFAULT_TIMEOUT)
                    await subpage.goto(job_link)
                    job_description = subpage.locator('div#ds')
                    job_description = await job_description.inner_text()
                    job_description = job_description[:3000] + (job_description[3000:] and '...')
                    await subpage.close()
                    job_data = JobData(job_company, job_title, job_description, job_link)
                    await super().notify(job_data)
                except Exception as ex:
                    print(ex)
            await page.goto(await jobpages.nth(j).get_attribute('href'))
        await page.close()
    
        