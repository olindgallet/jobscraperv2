# Author: Olin Gallet
# Date: 12/30/2022
from .websiteinterface import WebsiteInterface
from playwright.async_api import Browser
from .jobdata import JobData

class IndeedWebsite(WebsiteInterface):
    DATA_ANALYST_JOBS = 'https://www.indeed.com/jobs?q=data+analyst&l=remote&explvl=entry_level&sort=date&limit=50&fromage=1'
    BUSINESS_ANALYST_JOBS = 'https://www.indeed.com/jobs?q=business+analyst&l=remote&explvl=entry_level&sort=date&limit=50&fromage=1'
    MARKET_ANALYST_JOBS = 'https://www.indeed.com/jobs?q=market+analyst&l=remote&explvl=entry_level&sort=date&limit=50&fromage=1'
    FINANCIAL_ANALYST_JOBS = 'https://www.indeed.com/jobs?q=financial+analyst&l=remote&explvl=entry_level&sort=date&limit=50&fromage=1'
    #PYTHON_JOBS = 'https://www.indeed.com/jobs?q=python+developer&l=remote&explvl=entry_level&sort=date&limit=50&fromage=1'
    #JAVA_JOBS = 'https://www.indeed.com/jobs?q=java+developer&l=remote&explvl=entry_level&sort=date&fromage=1&limit=50'
    #JAVASCRIPT_JOBS = 'https://www.indeed.com/jobs?q=javascript+developer&l=remote&explvl=entry_level&sort=date&fromage=1&limit=50'
    #CURRICULUM_JOBS = 'https://www.indeed.com/jobs?q=curriculum&l=remote&sort=date&fromage=1&limit=50'
    #NOLA_JOBS = 'https://www.indeed.com/jobs?q=&l=New+Orleans%2C+LA&fromage=1&sort=date&limit=50'

    def __init__(self, url):
        super().__init__(url)

    async def scrape(self, browser:Browser):
        page = await browser.new_page()
        page.set_default_navigation_timeout(super()._DEFAULT_TIMEOUT)
        page.set_default_timeout(super()._DEFAULT_TIMEOUT)
        await page.goto(super().get_url())
        
        next_pages = page.locator('//nav[@role="navigation"]/div/a')
        for i in range(await next_pages.count() - 1):
            tables = page.locator('//table[contains(@class, "jobCard_mainContent")]')
            for j in range(await tables.count() - 1):
                try:
                    table = tables.nth(j)
                    job_company = await table.locator('xpath=tbody/tr/td/div/span[@class="companyName"]').inner_text()
                    job_company = job_company + ' @ ' + await table.locator('xpath=tbody/tr/td/div/div[@class="companyLocation"]').inner_text()
                    jlink = table.locator('xpath=tbody/tr/td/div/h2/a[starts-with(@class, "jcs-JobTitle")]')
                    job_title = await jlink.inner_text()
                    job_link = 'https://www.indeed.com' + await jlink.get_attribute('href')

                    subpage = await browser.new_page()
                    subpage.set_default_navigation_timeout(super()._DEFAULT_TIMEOUT)
                    subpage.set_default_timeout(super()._DEFAULT_TIMEOUT)
                    await subpage.goto(job_link)

                    job_description = subpage.locator('div#jobDescriptionText')
                    job_description = await job_description.inner_text()
                    job_description = job_description[:3000] + (job_description[3000:] and '...')
                    await subpage.close()

                    job_data = JobData(job_company, job_title, job_description, job_link)
                    await super().notify(job_data)
                except Exception as ex:
                    print(ex)

                if i < await next_pages.count():
                    await next_pages.nth(i + 1).click()
        await page.close()