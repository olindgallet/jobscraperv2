# Author: Olin Gallet
# Date: 5/11/2022
from .websiteinterface import WebsiteInterface
from playwright.async_api import Browser
from .jobdata import JobData

class CareerBuilderWebsite(WebsiteInterface):
    #REL_DATA_ANALYST_JOBS = 'https://www.careerbuilder.com/jobs?cb_apply=false&cb_veterans=false&cb_workhome=false&emp=&keywords=Data+Analyst&location=Boston&pay=&posted=1&sort=relevance_desc'
    #DAT_DATA_ANALYST_JOBS = 'https://www.careerbuilder.com/jobs?cb_apply=false&cb_veterans=false&cb_workhome=false&emp=&keywords=Data+Analyst&location=Boston&pay=&posted=1&sort=date_desc'
    
    REL_DATA_SCIENTIST_JOBS = 'https://www.careerbuilder.com/jobs?cb_apply=false&cb_workhome=false&emp=&keywords=Data+Scientist&location=Boston&pay=&posted=7&sort=relevance_desc'
    DAT_DATA_SCIENTIST_JOBS = 'https://www.careerbuilder.com/jobs?cb_apply=false&cb_workhome=false&emp=&keywords=Data+Scientist&location=Boston&pay=&posted=7&sort=date_desc'
    
    #REL_BUSINESS_ANALYST_JOBS = 'https://www.careerbuilder.com/jobs?cb_apply=false&cb_workhome=false&emp=&keywords=Business+Analyst&location=Boston&pay=&posted=1&sort=relevance_desc'
    #DAT_BUSINESS_ANALYST_JOBS = 'https://www.careerbuilder.com/jobs?cb_apply=false&cb_workhome=false&emp=&keywords=Business+Analyst&location=Boston&pay=&posted=1&sort=date_desc'
    
    #REL_ANALYTICS_JOBS = 'https://www.careerbuilder.com/jobs?cb_apply=false&cb_workhome=false&emp=&keywords=Analytics&location=Boston&pay=&posted=1&sort=relevance_desc'
    #DAT_ANALYTICS_JOBS = 'https://www.careerbuilder.com/jobs?cb_apply=false&cb_workhome=false&emp=&keywords=Analytics&location=Boston&pay=&posted=1&sort=date_desc'
    
    REL_DATA_ENGINEER_JOBS = 'https://www.careerbuilder.com/jobs?cb_apply=false&cb_workhome=false&emp=&keywords=Data+Engineer&location=Boston&pay=&posted=7&sort=relevance_desc'
    DAT_DATA_ENGINEER_JOBS = 'https://www.careerbuilder.com/jobs?cb_apply=false&cb_workhome=false&emp=&keywords=Data+Engineer&location=Boston&pay=&posted=7&sort=date_desc'

    REL_MACHINE_LEARNING_ENGINEER_JOBS = 'https://www.careerbuilder.com/jobs?cb_apply=false&cb_workhome=false&emp=&keywords=Machine+Learning+Engineer&location=Boston&pay=&posted=7&sort=relevance_desc'
    DAT_MACHINE_LEARNING_ENGINEER_JOBS = 'https://www.careerbuilder.com/jobs?cb_apply=false&cb_workhome=false&emp=&keywords=Machine+Learning+Engineer&location=Boston&pay=&posted=7&sort=date_desc'

    REL_ARTIFICIAL_INTELLIGENCE_ENGINEER_JOBS = 'https://www.careerbuilder.com/jobs?cb_apply=false&cb_workhome=false&emp=&keywords=Artificial+Intelligence+Engineer&location=Boston&pay=&posted=7&sort=relevance_desc'
    DAT_ARTIFICIAL_INTELLIGENCE_ENGINEER_JOBS = 'https://www.careerbuilder.com/jobs?cb_apply=false&cb_workhome=false&emp=&keywords=Artificial+Intelligence+Engineer&location=Boston&pay=&posted=7&sort=date_desc'

    REL_ARTIFICIAL_INTELLIGENCE_JOBS = 'https://www.careerbuilder.com/jobs?cb_apply=false&cb_workhome=false&emp=&keywords=Artificial+Intelligence&location=Boston&page_number={page_number}&pay=&posted=7&sort=relevance_desc'
    DAT_ARTIFICIAL_INTELLIGENCE_JOBS = 'https://www.careerbuilder.com/jobs?cb_apply=false&cb_workhome=false&emp=&keywords=Artificial+Intelligence&location=Boston&page_number={page_number}&pay=&posted=7&sort=date_desc'

    REL_MACHINE_LEARNING_JOBS = 'https://www.careerbuilder.com/jobs?cb_apply=false&cb_workhome=false&emp=&keywords=Machine+Learning&location=Boston&page_number={page_number}&pay=&posted=7&sort=relevance_desc'
    DAT_MACHINE_LEARNING_JOBS = 'https://www.careerbuilder.com/jobs?cb_apply=false&cb_workhome=false&emp=&keywords=Machine+Learning&location=Boston&page_number={page_number}&pay=&posted=7&sort=date_desc'

    REL_REAL_ESTATE_JOBS = 'https://www.careerbuilder.com/jobs?cb_apply=false&cb_workhome=false&emp=&keywords=Real+Estate&location=Boston&page_number={page_number}&pay=&posted=7&sort=relevance_desc'
    DAT_REAL_ESTATE_JOBS = 'https://www.careerbuilder.com/jobs?cb_apply=false&cb_workhome=false&emp=&keywords=Real+Estate&location=Boston&page_number={page_number}&pay=&posted=7&sort=date_desc'
    
    _BASE_URL = 'https://www.careerbuilder.com'
    
    def __init__(self, url):
        super().__init__(url)

    async def scrape(self, browser:Browser):
        page_number = 1
        while True:
            page = await browser.new_page()
            await page.goto(super().get_url(), timeout=0)
            await page.wait_for_selector('ol#jobs_collection')
            joblist = page.locator('ol#jobs_collection').locator('li')

            job_count = await joblist.count()
            if job_count == 0:
                print("No more jobs found.")
                break  # Exit the loop if no jobs are found

            for i in range(await joblist.count() - 1):
                try:
                    job_title = await joblist.nth(i).locator('xpath=div/div/div[contains(@class, "data-results-title")]').inner_text()   
                    job_company = await joblist.nth(i).locator('xpath=div/div/div/span').nth(0).inner_text()  
                    job_link = self._BASE_URL + await joblist.nth(i).locator('a').get_attribute('href')
                    job_location = await joblist.nth(i).locator('xpath=div/div/div/span').nth(1).inner_text()
                    
                    #subpage = await browser.new_page()
                    #await subpage.goto(job_link, timeout=0)
                    #job_description = subpage.locator('div#jdp_description')
                    #job_description = await job_description.inner_text()
                    job_description = "job description" #job_description[:99999] + (job_description[99999:] and '...')
                    #await subpage.close()

                    job_data = JobData(job_company, job_title, job_description, job_link, job_location)
                    await super().notify(job_data)
                except Exception as ex:
                    print(ex)

            # Increment the page number
            page_number += 1
            await page.close()
    
        