# Author: Olin Gallet
# Date: 12/30/2022
from .websiteinterface import WebsiteInterface
from playwright.async_api import Browser
from .jobdata import JobData
import random

class IndeedWebsite(WebsiteInterface):
    #DATA_ANALYST_JOBS = 'https://www.indeed.com/jobs?q=data+analyst&l=Boston&radius=35&sort=date&limit=50&fromage=1'
    #BUSINESS_ANALYST_JOBS = 'https://www.indeed.com/jobs?q=business+analyst&l=Boston&radius=35&sort=date&limit=50&fromage=1'
    #DATA_SCIENTIST_JOBS = 'https://www.indeed.com/jobs?q=data+scientist&l=Boston&radius=35&sort=date&limit=50&fromage=1'
    #ANALYTICS_JOBS = 'https://www.indeed.com/jobs?q=analytics&l=Boston&radius=35&sort=date&limit=50&fromage=1'
    #DATA_ENGINEER_JOBS = 'https://www.indeed.com/jobs?q=data+engineer&l=Boston&radius=35&sort=date&limit=50&fromage=1'
    ARTIFICIAL_INTELLIGENCE_JOBS = 'https://www.indeed.com/jobs?q=artificial+intelligence&l=Boston&radius=35&sort=date&limit=50&fromage=1'

    #PYTHON_JOBS = 'https://www.indeed.com/jobs?q=python+developer&l=Boston&radius=35&sort=date&limit=50&fromage=1'
    #JAVA_JOBS = 'https://www.indeed.com/jobs?q=java+developer&l=Boston&radius=35&sort=date&fromage=1&limit=50'
    #JAVASCRIPT_JOBS = 'https://www.indeed.com/jobs?q=javascript+developer&l=Boston&radius=35&sort=date&fromage=1&limit=50'
    #CURRICULUM_JOBS = 'https://www.indeed.com/jobs?q=curriculum&l=remote&sort=date&fromage=1&limit=50'
    #NOLA_JOBS = 'https://www.indeed.com/jobs?q=&l=New+Orleans%2C+LA&fromage=1&sort=date&limit=50'

    def __init__(self, url):
        super().__init__(url)

    async def scrape(self, browser:Browser):
        page = await browser.new_page()
        #await page.screenshot(path='debug_screenshot.png')
        await page.mouse.move(100, 100)
        await page.mouse.down()
        await page.wait_for_timeout(500 + random.randint(100, 500))  # Randomize wait times.
        page.set_default_navigation_timeout(super()._DEFAULT_TIMEOUT)
        page.set_default_timeout(super()._DEFAULT_TIMEOUT)
        await page.goto(super().get_url())
        #await page.screenshot(path='debug_screenshot2.png')
        await page.wait_for_timeout(5000 + random.randint(100, 500))  # Randomize wait times.
        await page.mouse.move(100, 100)
        await page.mouse.down()
        await page.wait_for_timeout(500 + random.randint(100, 500))  # Randomize wait times.
        #await page.screenshot(path='debug_screenshot3.png')
        await page.wait_for_timeout(500 + random.randint(100, 500))  # Randomize wait times.
        await page.screenshot(path='debug_screenshot4.png')
        await page.wait_for_timeout(500 + random.randint(100, 500))  # Randomize wait times.

        # Print the HTML of the page
        html_content = await page.content()
        print("html:", html_content)  # This will print the entire HTML content to your console

        # Try to locate the iframe by its title
        iframe_selector = 'iframe[title="Widget containing a Cloudflare security challenge"]'
        iframe_element = await page.wait_for_selector(iframe_selector, state="attached", timeout=60000)
        frame = await iframe_element.content_frame()

        await page.screenshot(path='debug_screenshot6.png')

        # Assuming you know the selector of the checkbox inside the iframe
        checkbox_selector = 'input[type="checkbox"]'  # Update this if the actual selector is different
        checkbox = await frame.wait_for_selector(checkbox_selector, timeout=60000)
        await checkbox.check()  # Check the checkbox

        # Optionally, add another screenshot to confirm the checkbox has been clicked
        await page.screenshot(path='debug_screenshot7.png')

        
        next_pages = page.locator('//nav[@role="navigation"]/div/a')
        tables = page.locator('//table[contains(@class, "jobCard_mainContent")]')
        for i in range(await tables.count() - 1):
            try:
                table = tables.nth(i)
                job_company = await table.locator('xpath=tbody/tr/td/div/span[@class="companyName"]').inner_text()
                job_company = job_company + ' @ ' + await table.locator('xpath=tbody/tr/td/div/div[@class="companyLocation"]').inner_text()
                #job_location = await table.locator('xpath=tbody/tr/td/div/div[@class="companyLocation"]').inner_text()
                job_location = job_company
                jlink = table.locator('xpath=tbody/tr/td/div/h2/a[starts-with(@class, "jcs-JobTitle")]')
                job_title = await jlink.inner_text()
                job_link = 'https://www.indeed.com' + await jlink.get_attribute('href')

                subpage = await browser.new_page()
                subpage.set_default_navigation_timeout(super()._DEFAULT_TIMEOUT)
                subpage.set_default_timeout(super()._DEFAULT_TIMEOUT)
                await subpage.goto(job_link)

                job_description = subpage.locator('div#jobDescriptionText')
                job_description = await job_description.inner_text()
                job_description = job_description[:99999] + (job_description[99999:] and '...')
                await subpage.close()

                job_data = JobData(job_company, job_title, job_description, job_link, job_location)
                await super().notify(job_data)
            except Exception as ex:
                print(ex)
        await page.close()