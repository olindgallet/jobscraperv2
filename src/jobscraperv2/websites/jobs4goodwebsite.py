# Author: Olin Gallet
# Date: 18/1/2023
from .websiteinterface import WebsiteInterface
from playwright.async_api import Browser
from .jobdata import JobData
import time

class Jobs4GoodWebsite(WebsiteInterface):
    #GRETNA_JOBS = "https://www.learn4good.com/jobs/9764/gretna/la-louisiana/area/"
    #HARVEY_JOBS = "https://www.learn4good.com/jobs/9769/harvey/la-louisiana/area/"
    #MARRERO_JOBS = "https://www.learn4good.com/jobs/9777/marrero/la-louisiana/area/"
    #NEW_ORLEANS_JOBS = "https://www.learn4good.com/jobs/9787/new-orleans/la-louisiana/area/"
    #WESTWEGO_JOBS = "https://www.learn4good.com/jobs/9741/westwego/la-louisiana/area/"
    BOSTON_JOBS = "https://www.learn4good.com/jobs/"


    _MAX_PAGES_CRAWLED = 100

    def __init__(self, url):
        super().__init__(url)

    async def scrape(self, browser:Browser):

        KEYWORD = 'Real Estate'

        page = await browser.new_page()
        page.set_default_navigation_timeout(super()._DEFAULT_TIMEOUT)
        page.set_default_timeout(super()._DEFAULT_TIMEOUT)
        await page.goto(super().get_url())
        # Select the button by its XPath and click it
        button_selector = '//*[@id="cookies_agree"]'
        await page.click(button_selector)

        # Wait for the iframe to load, and then switch to the iframe context
        iframe = await page.wait_for_selector('iframe[title="Sign in with Google Dialog"]')
        frame = await iframe.content_frame()

        # Click the button inside the iframe
        button_selector = '#close'  # ID selector for the button
        await frame.click(button_selector)

        input_selector = 'input[placeholder="Type in a skill or profession"]'
        await page.fill(input_selector, KEYWORD)

        # Click the label that acts as a button
        button_selector = 'label.extend_button.for_job'  # Using the class to select the label
        await page.click(button_selector)

        time.sleep(5)

        jobpages = page.locator('div[class="pagination"]').locator('a')
        await page.screenshot(path='debug_screenshot11.png')
        job_location = 'No Location Found'
            
        for j in range(self._MAX_PAGES_CRAWLED):
            joblist = page.locator('table#main_job_list').locator('tr')
            for i in range(await joblist.count() - 1):
                try:
                    job_link = await joblist.nth(i).locator('a[class="job_title"]').get_attribute('href')
                    job_title = await joblist.nth(i).locator('a[class="job_title"]').inner_text()
                    print("job title: ", job_title)
                    job_company = await joblist.nth(i).locator('span[class="absent_link"]').inner_text() # + ' @ ' + job_location
                    job_description = 'No description available.'
                    job_location = await joblist.nth(i).locator('h3[class="loc_title"]').inner_text()
                    job_data = JobData(job_company, job_title, job_description, job_link, job_location)
                    await super().notify(job_data)
                except Exception as ex:
                    print(ex)
            await page.goto(await jobpages.nth(j).get_attribute('href'))
        await page.close()