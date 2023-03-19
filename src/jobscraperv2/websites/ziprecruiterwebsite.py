# Author: Olin Gallet
# Date: 5/11/2022
from .websiteinterface import WebsiteInterface
from playwright.async_api import Browser
from .jobdata import JobData
import os

class ZipRecruiterWebsite(WebsiteInterface):
    DATA_ANALYST_JOBS = 'https://www.ziprecruiter.com/jobs-search?search=Junior+Data+Analyst&location=Remote+%28USA%29&refine_by_location_type=only_remote&radius=25&days=1'
    BUSINESS_ANALYST_JOBS = 'https://www.ziprecruiter.com/jobs-search?search=Junior+Business+Analyst&location=Remote+%28USA%29&refine_by_location_type=only_remote&radius=25&days=1'
    ANALYTICS_JOBS = 'https://www.ziprecruiter.com/jobs-search?search=data+analytics&location=Remote+%28USA%29&refine_by_location_type=only_remote&radius=25&days=1'
    DATA_SCIENTIST_JOBS = 'https://www.ziprecruiter.com/jobs-search?search=Junior+Data+Scientist&location=Remote+%28USA%29&refine_by_location_type=only_remote&radius=25&days=1'
    DATA_ENGINEER_JOBS = 'https://www.ziprecruiter.com/jobs-search?search=Junior+Data+Engineer&location=Remote+%28USA%29&refine_by_location_type=only_remote&radius=25&days=1'

    LOGIN_PAGE = 'https://www.ziprecruiter.com/authn/login'             
    def __init__(self, url):
        super().__init__(url)

    async def scrape(self, browser:Browser):
        page = await browser.new_page()

        await page.goto(self.LOGIN_PAGE)
        await page.locator('input#email').fill(os.environ['ZIP_RECRUITER_LOGIN'])
        await page.locator('input#password').fill(os.environ['ZIP_RECRUITER_PASSWORD'])
        await page.locator('button#submit_button').click()

        await page.goto(super().get_url(), timeout=0)

        await page.wait_for_selector('div#job_postings_skip')
        joblist = page.locator('div#job_postings_skip').locator('article')

        for i in range(await joblist.count() - 1):
            try:
                job_title = await joblist.nth(i).locator('a[class="job_link"]').inner_text()
                job_link = await joblist.nth(i).locator('a[class="job_link"]').get_attribute('href')
                job_company = await joblist.nth(i).locator('a[class="company_name"]').inner_text()
                
                subpage = await browser.new_page()
                await subpage.goto(job_link, timeout=0)
                page.set_default_timeout(5000)
                job_description = "Job data unable to be scraped."
                try:
                    job_description = subpage.locator('div[class="jobDescriptionSection"]')
                    job_description = await job_description.inner_text()
                    job_description = job_description[:99999] + (job_description[99999:] and '...')
                except Exception as ex:
                    job_description = "Job data unable to be scraped."
                await subpage.close()

                job_data = JobData(job_company, job_title, job_description, job_link)
                await super().notify(job_data)
            except Exception as ex:
                print(ex)
        await page.close()
    
        