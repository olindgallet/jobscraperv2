# Author: Olin Gallet
# Date: 5/11/2022
from .websiteinterface import WebsiteInterface
from playwright.async_api import Browser
from .jobdata import JobData

class DiceWebsite(WebsiteInterface):
    #PYTHON_JOBS = 'https://www.dice.com/jobs?q=python%20&countryCode=US&radius=30&radiusUnit=mi&page=1&pageSize=100&filters.postedDate=ONE&filters.isRemote=true&language=en'
    #JAVA_JOBS = 'https://www.dice.com/jobs?q=java&countryCode=US&radius=30&radiusUnit=mi&page=1&pageSize=100&filters.postedDate=ONE&filters.isRemote=true&language=en&eid=S2Q_'
    #JAVASCRIPT_JOBS = 'https://www.dice.com/jobs?q=javascript&countryCode=US&radius=30&radiusUnit=mi&page=1&pageSize=100&filters.postedDate=ONE&filters.isRemote=true&language=en&eid=S2Q_'
    DATA_ANALYST_JOBS = 'https://www.dice.com/jobs?q=data%20analyst&countryCode=US&radius=30&radiusUnit=mi&page=1&pageSize=100&filters.postedDate=THREE&filters.employmentType=FULLTIME&filters.isRemote=true&language=en'

    def __init__(self, url):
        super().__init__(url)

    async def scrape(self, browser:Browser):
        page = await browser.new_page()
        await page.goto(super().get_url(), timeout=0)
        await page.wait_for_selector('div#searchDisplay-div')
        keep_going = True
        while keep_going:
            joblist = page.locator('h5')
            for i in range(await joblist.count() - 1):
                try:
                    if 'Dice' not in await joblist.nth(i).inner_text() and \
                    await joblist.nth(i).locator('xpath=a').count() > 0 and \
                    await joblist.nth(i).locator('xpath=parent::div/div/a').count() > 0:                      
                        job_link = await joblist.nth(i).locator('a').get_attribute('href')
                        job_title = await joblist.nth(i).inner_text()
                        job_company = await joblist.nth(i).locator('xpath=parent::div/div/a').inner_text()

                        subpage = await browser.new_page()
                        await subpage.goto(job_link, timeout=0)
                        job_description = subpage.locator('div#jobDescription')
                        job_description = await job_description.inner_text()
                        job_description = job_description[:3000] + (job_description[3000:] and '...')
                        await subpage.close()
                        job_data = JobData(job_company, job_title, job_description, job_link)
                        await super().notify(job_data)
                except Exception as ex:
                    print(ex)
            next = page.get_by_text('»')
            if 'disabled' not in await next.get_attribute('class'):
                await next.click()
            else:
                keep_going = False
        await page.close()
    
        