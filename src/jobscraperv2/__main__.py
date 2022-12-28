# Author: Olin Gallet
# Date: 6/11/2022
 
from .websites.dicewebsite import DiceWebsite
from playwright.async_api import async_playwright
from .websites.observers.airtableasobserver import AirtableAsObserver
from .websites.observers.terminalasobserver import TerminalAsObserver
from .util import terminal 
import asyncio
import sys

async def main(use_terminal, use_airtable):
    playwright = await async_playwright().start()
    site = DiceWebsite()
    if use_terminal:
        site.subscribe(TerminalAsObserver())
    if use_airtable:
        site.subscribe(AirtableAsObserver())
    browser = await playwright.chromium.launch()  
    await site.scrape(browser, DiceWebsite.PYTHON_JOBS)
    await browser.close()
    await playwright.stop()

if __name__ == '__main__':
    use_terminal = False
    use_airtable = False
    if '-a' not in sys.argv and '-t' not in sys.argv:
        terminal.Terminal.display_usage_help()
    else:    
        if '-a' in sys.argv:
            use_airtable = True
        if '-t' in sys.argv:
            use_terminal = True
        asyncio.run(main(use_terminal, use_airtable))