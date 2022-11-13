# Author: Olin Gallet
# Date: 6/11/2022
 
from websites import dicewebsite as dice
from playwright.async_api import async_playwright
from websites.observers.airtableasobserver import AirtableAsObserver
from websites.observers.terminalasobserver import TerminalAsObserver
import asyncio
import sys

async def main(use_terminal, use_airtable):
    playwright = await async_playwright().start()
    site = dice.DiceWebsite()
    if use_terminal:
        site.subscribe(TerminalAsObserver())
    if use_airtable:
        site.subscribe(AirtableAsObserver())
    browser = await playwright.chromium.launch()  
    await site.scrape(browser, dice.DiceWebsite.PYTHON_JOBS)
    await browser.close()
    await playwright.stop()

if __name__ == '__main__':
    use_terminal = False
    use_airtable = False
    if '-a' in sys.argv:
        use_airtable = True
    if '-t' in sys.argv:
        use_terminal = True
    asyncio.run(main(use_terminal, use_airtable))