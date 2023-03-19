# Author: Olin Gallet
# Date: 5/11/2022
from .websiteinterface import WebsiteInterface
from playwright.async_api import Browser
from .jobdata import JobData

class CareerBuilderWebsite(WebsiteInterface):
    REL_DATA_ANALYST_JOBS = 'https://www.careerbuilder.com/jobs?cb_apply=false&cb_veterans=false&cb_workhome=true&emp=&keywords=Data+Analyst&location=Work+from+Home%2FRemote&pay=&posted=1&sort=relevance_desc'
    DAT_DATA_ANALYST_JOBS = 'https://www.careerbuilder.com/jobs?cb_apply=false&cb_veterans=false&cb_workhome=true&emp=&keywords=Data+Analyst&location=Work+from+Home%2FRemote&pay=&posted=1&sort=date_desc'
    
    REL_DATA_SCIENTIST_JOBS = 'https://www.careerbuilder.com/jobs?cb_apply=false&cb_workhome=true&emp=&keywords=Data+Scientist&location=Work+from+Home%2FRemote&pay=&posted=1&sort=relevance_desc'
    DAT_DATA_SCIENTIST_JOBS = 'https://www.careerbuilder.com/jobs?cb_apply=false&cb_workhome=true&emp=&keywords=Data+Scientist&location=Work+from+Home%2FRemote&pay=&posted=1&sort=date_desc'
    
    REL_BUSINESS_ANALYST_JOBS = 'https://www.careerbuilder.com/jobs?cb_apply=false&cb_workhome=true&emp=&keywords=Business+Analyst&location=Work+from+Home%2FRemote&pay=&posted=1&sort=relevance_desc'
    DAT_BUSINESS_ANALYST_JOBS = 'https://www.careerbuilder.com/jobs?cb_apply=false&cb_workhome=true&emp=&keywords=Business+Analyst&location=Work+from+Home%2FRemote&pay=&posted=1&sort=date_desc'
    
    REL_ANALYTICS_JOBS = 'https://www.careerbuilder.com/jobs?cb_apply=false&cb_workhome=true&emp=&keywords=Analytics&location=Work+from+Home%2FRemote&pay=&posted=1&sort=relevance_desc'
    DAT_ANALYTICS_JOBS = 'https://www.careerbuilder.com/jobs?cb_apply=false&cb_workhome=true&emp=&keywords=Analytics&location=Work+from+Home%2FRemote&pay=&posted=1&sort=date_desc'
    
    REL_DATA_ENGINEER_JOBS = 'https://www.careerbuilder.com/jobs?cb_apply=false&cb_workhome=true&emp=&keywords=Data+Engineer&location=Work+from+Home%2FRemote&pay=&posted=1&sort=relevance_desc'
    DAT_DATA_ENGINEER_JOBS = 'https://www.careerbuilder.com/jobs?cb_apply=false&cb_workhome=true&emp=&keywords=Data+Engineer&location=Work+from+Home%2FRemote&pay=&posted=1&sort=date_desc'
    
    _BASE_URL = 'https://www.careerbuilder.com'
    
    def __init__(self, url):
        super().__init__(url)

    async def scrape(self, browser:Browser):
        page = await browser.new_page()
        await page.goto(super().get_url(), timeout=0)
        await page.wait_for_selector('ol#jobs_collection')
        joblist = page.locator('ol#jobs_collection').locator('li')
        for i in range(await joblist.count() - 1):
            try:
                job_title = await joblist.nth(i).locator('xpath=div/div/div[contains(@class, "data-results-title")]').inner_text()   
                job_company = await joblist.nth(i).locator('xpath=div/div/div/span').nth(0).inner_text() 
                job_link = self._BASE_URL + await joblist.nth(i).locator('a').get_attribute('href')
                
                subpage = await browser.new_page()
                await subpage.goto(job_link, timeout=0)
                job_description = subpage.locator('div#jdp_description')
                job_description = await job_description.inner_text()
                job_description = job_description[:99999] + (job_description[99999:] and '...')
                await subpage.close()

                job_data = JobData(job_company, job_title, job_description, job_link)
                await super().notify(job_data)
            except Exception as ex:
                print(ex)
        await page.close()
    
        