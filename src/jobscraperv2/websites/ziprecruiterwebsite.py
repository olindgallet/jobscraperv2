# Author: Olin Gallet
# Date: 20/3/2022
from .websiteinterface import WebsiteInterface
from playwright.async_api import Browser
from .jobdata import JobData
import os
from dotenv import load_dotenv, find_dotenv
import time
import json
import re

class ZipRecruiterWebsite(WebsiteInterface):
    #DATA_ANALYST_JOBS = 'https://www.ziprecruiter.com/jobs-search?search=Junior+Data+Analyst&location=Remote+%28USA%29&refine_by_location_type=only_remote&radius=25&days=1'
    #BUSINESS_ANALYST_JOBS = 'https://www.ziprecruiter.com/jobs-search?search=Junior+Business+Analyst&location=Remote+%28USA%29&refine_by_location_type=only_remote&radius=25&days=1'
    #ANALYTICS_JOBS = 'https://www.ziprecruiter.com/jobs-search?search=data+analytics&location=Remote+%28USA%29&refine_by_location_type=only_remote&radius=25&days=1'
    #DATA_SCIENTIST_JOBS = 'https://www.ziprecruiter.com/jobs-search?search=Junior+Data+Scientist&location=Remote+%28USA%29&refine_by_location_type=only_remote&radius=25&days=1'
    #DATA_ENGINEER_JOBS = 'https://www.ziprecruiter.com/jobs-search?search=Junior+Data+Engineer&location=Remote+%28USA%29&refine_by_location_type=only_remote&radius=25&days=1'
    ARTIFICIAL_INTELLIGENCE_JOBS = 'https://www.ziprecruiter.com/jobs-search?search=Artificial+Intelligence&location=Boston+%28USA%29&radius=25&days=7'
    MACHINE_LEARNING_JOBS = 'https://www.ziprecruiter.com/jobs-search?search=Machine+Learning&location=Boston+%28USA%29&radius=25&days=7'
    REAL_ESTATE_JOBS = 'https://www.ziprecruiter.com/jobs-search?search=Real+Estate&location=Boston+%28USA%29&radius=25&days=7'


    LOGIN_PAGE = 'https://www.ziprecruiter.com/authn/login'             
    def __init__(self, url):
        super().__init__(url)

    async def scrape(self, browser:Browser):
        load_dotenv(find_dotenv())
        page = await browser.new_page()
        await page.goto(self.LOGIN_PAGE, wait_until="networkidle")
        await page.locator('input#email').fill(os.environ['ZIP_RECRUITER_LOGIN'])
        await page.locator('input#password').fill(os.environ['ZIP_RECRUITER_PASSWORD'])
        await page.locator('button#submit_button').click()
        time.sleep(2)

        await page.goto(super().get_url(), timeout=0)
        time.sleep(4)

        current_page = 1
        while True:

            await page.wait_for_selector('div.site_content')
            time.sleep(2)

            html_content = await page.content()
            matches = re.findall(r'<script id="js_variables" type="application/json"[^>]*>(.*?)</script>', html_content, re.DOTALL)

            if matches:
                # Assuming the first match is the one we're interested in
                json_data = json.loads(matches[0])
                # Navigate the JSON object to extract job titles
                job_list = json_data.get('jobList', [])
                for job in job_list:
                    print("job: ", job)
                    job_title = job.get('Title')
                    job_company = job.get('OrgName')
                    job_link = job.get('JobURL')
                    job_location = job.get('City')
                    job_description = 'job_description'
                    job_data = JobData(job_company, job_title, job_description, job_link, job_location)
                    await super().notify(job_data)
                    
            else:
                print("No job data found in the script tags")

            # Try to find the next page button and click it if present
            next_page_button = await page.query_selector('a[title="Next Page"]')
            if next_page_button:
                await next_page_button.click()
                print(f"Moving to page {current_page + 1}")
                current_page += 1
                await page.wait_for_load_state('networkidle')  # Ensure the next page has loaded
            else:
                print("No more pages to scrape.")