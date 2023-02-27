# Author: Olin Gallet
# Date: 6/11/2022
 
from .websites.weworkremotelywebsite import WeWorkRemotelyWebsite as wwr
from .websites.indeedwebsite import IndeedWebsite as indeed
from .websites.hitmarkerwebsite import HitMarkerWebsite as hitma
from .websites.dicewebsite import DiceWebsite as dice
from playwright.async_api import async_playwright
from .websites.observers.airtableasobserver import AirtableAsObserver
from .websites.observers.terminalasobserver import TerminalAsObserver
from .util.terminal import Terminal
import asyncio
import sys

async def main(use_terminal, use_airtable):
    playwright = await async_playwright().start()
    #sites = [indeed(indeed.DATA_ANALYST_JOBS),
    #         indeed(indeed.BUSINESS_ANALYST_JOBS),
    #         indeed(indeed.MARKET_ANALYST_JOBS),
    #         indeed(indeed.FINANCIAL_ANALYST_JOBS),
    #sites = [wwr(wwr.DATA_JOBS)]
    #sites = [hitma(hitma.DATA_JOBS)]
    #sites = [dice(dice.DATA_ANALYST_JOBS)]
    for site in sites:
        browser = None
        try:
            if use_terminal:
                site.subscribe(TerminalAsObserver())
            if use_airtable:
                site.subscribe(AirtableAsObserver())
            browser = await playwright.chromium.launch()  
            await site.scrape(browser)
            await browser.close()
        except Exception as e:
            Terminal.display_website_error(site.get_url(), e.message)
            if browser is not None:
                await browser.close()
    await playwright.stop()

def execute():
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

if __name__ == '__main__':
    execute()