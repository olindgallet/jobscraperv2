# Author: Olin Gallet
# Date: 5/11/2022
from .websiteinterface import WebsiteInterface
from playwright.async_api import Browser
from .jobdata import JobData
import random

class DiceWebsite(WebsiteInterface):

    posted_date = 'SEVEN'
    location = 'Boston,%20MA,%20USA&latitude=42.3600825&longitude=-71.0588801&countryCode=US&locationPrecision=City&adminDistrictCode=MA&radius=30&radiusUnit=mi'

    ARTIFICIAL_INTELLIGENCE_JOBS = 'https://www.dice.com/jobs?q=artificial%20intelligence&location=Boston,%20MA,%20USA&latitude=42.3600825&longitude=-71.0588801&countryCode=US&locationPrecision=City&adminDistrictCode=MA&radius=30&radiusUnit=mi&page={page}&pageSize=100&filters.postedDate=SEVEN&filters.employmentType=FULLTIME&filters.isRemote=false&language=en'
    MACHINE_LEARNING_JOBS = 'https://www.dice.com/jobs?q=machine%20learning&location=Boston,%20MA,%20USA&latitude=42.3600825&longitude=-71.0588801&countryCode=US&locationPrecision=City&adminDistrictCode=MA&radius=30&radiusUnit=mi&page={page}&pageSize=100&filters.postedDate=SEVEN&filters.employmentType=FULLTIME&filters.isRemote=false&language=en'
    REAL_ESTATE_JOBS = 'https://www.dice.com/jobs?q=real%20estate&location=Boston,%20MA,%20USA&latitude=42.3600825&longitude=-71.0588801&countryCode=US&locationPrecision=City&adminDistrictCode=MA&radius=30&radiusUnit=mi&page={page}&pageSize=100&filters.postedDate=SEVEN&filters.employmentType=FULLTIME&filters.isRemote=false&language=en'


    def __init__(self, url):
        super().__init__(url)
        if not url:  # Check if URL is None or empty
            raise ValueError("URL must not be empty")

    async def scrape(self, browser: Browser):
        for page_number in range(1, 5):  # Loop through pages 1 to 4
            page_url = self._url.format(page=page_number)

            page = await browser.new_page()
            await page.screenshot(path='debug_screenshot1.png')
            if not page_url:
                raise ValueError("URL is not set for scraping")
            print(f"Going to URL: {page_url}")  # Debug print to check what URL is being passed
            await page.wait_for_timeout(5000 + random.randint(100, 500))  # Randomize wait times.
            await page.goto(page_url, timeout=0, wait_until="networkidle")
            await page.wait_for_timeout(5000 + random.randint(100, 500))  # Randomize wait times.
            await page.screenshot(path='debug_screenshot2.png')
            await page.wait_for_timeout(5000 + random.randint(100, 500))  # Randomize wait times.
            await page.wait_for_selector('div#searchDisplay-div')
            await page.wait_for_timeout(1000)  # waits for 1 second; adjust as needed
            joblist = page.locator('h5')
            await page.wait_for_timeout(1000)  # waits for 1 second; adjust as needed
            for i in range(await joblist.count() - 1):
                try:
                    if 'Dice' not in await joblist.nth(i).inner_text() and \
                    await joblist.nth(i).locator('xpath=a').count() > 0 and \
                    await joblist.nth(i).locator('xpath=parent::div/div/a').count() > 0:   
                        await page.wait_for_timeout(1000)  # waits for 1 second; adjust as needed                   
                        job_link = page_url #joblist.nth(i).locator('a')#.get_attribute('href')
                        #JOB LINK NOT WORKING, LINK IS JUST LINK FOR SEARCH CRITERIA
                        job_title = await joblist.nth(i).inner_text()
                        job_company = await joblist.nth(i).locator('xpath=parent::div/div/a').inner_text()
                        job_location =  await joblist.nth(i).locator('xpath=parent::div/div/span').inner_text()
                        job_description = "job description"
                        job_data = JobData(job_company, job_title, job_description, job_link, job_location)
                        print(f"Notifying observers with job data for {job_title}")
                        await super().notify(job_data)
                except Exception as ex:
                    print(ex)
            await page.close()