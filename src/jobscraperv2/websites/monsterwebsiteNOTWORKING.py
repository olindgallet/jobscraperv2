# Author: Olin Gallet
# Date: 20/3/2023
from .websiteinterface import WebsiteInterface
from playwright.async_api import Browser
from .jobdata import JobData
import random
import time

class MonsterWebsite(WebsiteInterface):
    DATA_ANALYST_JOBS = 'https://www.monster.com/jobs/search?q=Data+Analyst&where=remote&page=1&et=FULL_TIME&et=REMOTE&recency=last+2+days&so=m.h.s'
    DATA_SCIENTIST_JOBS = 'https://www.monster.com/jobs/search?q=Data+Scientist&where=remote&page=1&et=FULL_TIME&et=REMOTE&recency=last+2+days&so=m.h.s'
    DATA_ENGINEER_JOBS = 'https://www.monster.com/jobs/search?q=Data+Engineer&where=remote&page=1&et=FULL_TIME&et=REMOTE&recency=last+2+days&so=m.h.s'
    BUSINESS_ANALYST_JOBS = 'https://www.monster.com/jobs/search?q=Business+Analyst&where=remote&page=1&et=FULL_TIME&et=REMOTE&recency=last+2+days&so=m.h.s'
    ANALYTICS_JOBS = 'https://www.monster.com/jobs/search?q=Analytics&where=remote&page=1&et=FULL_TIME&et=REMOTE&recency=last+2+days&so=m.h.s'
    ARTIFICIAL_INTELLIGENCE_JOBS = 'https://www.monster.com/jobs/search?q=Artificial+Intelligence&where=remote&page=1&et=FULL_TIME&et=REMOTE&recency=last+2+days&so=m.h.s'

    def __init__(self, url):
        super().__init__(url)

    async def scrape(self, browser:Browser):
        page = await browser.new_page()
        await page.goto(super().get_url(), timeout=0)
        await page.screenshot(path='debug_screenshot1.png')
        await page.wait_for_timeout(500 + random.randint(100, 500))  # Randomize wait times.
        time.sleep(10)
        await page.screenshot(path='debug_screenshot15.png')
        await page.wait_for_selector('div#JobCardGrid')
        await page.locator('div#JobCardGrid').click()
        await page.screenshot(path='debug_screenshot2.png')
        while await page.locator("button",has_text="No More Results").is_visible() is False:
            await page.mouse.wheel(0,200)
        await page.wait_for_selector('article') 
        await page.screenshot(path='debug_screenshot3.png')
        joblist = page.locator('article')
        for i in range(0, await joblist.count() - 1):
            try:
                job_title = await joblist.nth(i).locator('xpath=div/a').inner_text()
                job_link = 'https:' + await joblist.nth(i).locator('xpath=div/a').get_attribute('href')
                job_company = await joblist.nth(i).locator('xpath=div/h3').inner_text()

                await joblist.nth(i).click()
                await page.wait_for_selector('div#BigJobCardId')
                job_description = await page.locator('div#BigJobCardId').inner_text()
                job_description = job_description[:99999] + (job_description[99999:] and '...')

                print(job_title)
                print(job_company)
                print(job_link)
                print(job_description)
            except Exception as ex:
                print(ex)
        await page.close()
    
        