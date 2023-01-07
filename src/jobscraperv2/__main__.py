# Author: Olin Gallet
# Date: 6/11/2022
 
from .websites.dicewebsite import DiceWebsite as dice
from .websites.weworkremotelywebsite import WeWorkRemotelyWebsite as wwr
from .websites.indeedwebsite import IndeedWebsite as indeed
from playwright.async_api import async_playwright
from .websites.observers.airtableasobserver import AirtableAsObserver
from .websites.observers.terminalasobserver import TerminalAsObserver
from .util.terminal import Terminal
import asyncio
import sys

async def main(use_terminal, use_airtable):
    playwright = await async_playwright().start()
    sites = [indeed(indeed.NOLA_JOBS),
             indeed(indeed.PYTHON_JOBS),
             indeed(indeed.JAVA_JOBS),
             indeed(indeed.JAVASCRIPT_JOBS),
             indeed(indeed.CURRICULUM_JOBS),
             wwr(wwr.FRONT_END_PROGRAMMING_JOBS), 
             wwr(wwr.BACK_END_PROGRAMMING_JOBS), 
             wwr(wwr.SYS_ADMIN_JOBS),
             wwr(wwr.FULL_STACK_PROGRAMMING_JOBS),
             wwr(wwr.CUSTOMER_SUPPORT_JOBS),
             wwr(wwr.PRODUCT_JOBS),
             dice(dice.PYTHON_JOBS),
             dice(dice.JAVA_JOBS),
             dice(dice.JAVASCRIPT_JOBS)]
    for site in sites:
        browser = None
        try:
            if use_terminal:
                site.subscribe(TerminalAsObserver())
            if use_airtable:
                site.subscribe(AirtableAsObserver())
            browser = await playwright.firefox.launch()  
            await site.scrape(browser)
            await browser.close()
        except Exception as e:
            Terminal.display_website_error(site.get_url(), e.message)
            if browser is not None:
                await browser.close()
    await playwright.stop()
    
if __name__ == '__main__':
    use_terminal = False
    use_airtable = False
    if '-a' not in sys.argv and '-t' not in sys.argv:
        Terminal.display_usage_help()
    else:    
        if '-a' in sys.argv:
            use_airtable = True
        if '-t' in sys.argv:
            use_terminal = True
        asyncio.run(main(use_terminal, use_airtable))