# Author: Olin Gallet
# Date: 6/11/2022
 
from .websites.weworkremotelywebsite import WeWorkRemotelyWebsite as wwr
from .websites.indeedwebsite import IndeedWebsite as indeed
from .websites.hitmarkerwebsite import HitMarkerWebsite as hitma
from .websites.dicewebsite import DiceWebsite as dice
from .websites.himalayaswebsite import HimalayasWebsite as himalayas
from .websites.nowhiteboardwebsite import NoWhiteboardWebsite as nowb
from .websites.careerbuilderwebsite import CareerBuilderWebsite as cb
from .websites.ziprecruiterwebsite import ZipRecruiterWebsite as zip
from .websites.monsterwebsite import MonsterWebsite as monster
from playwright.async_api import async_playwright
from .websites.observers.airtableasobserver import AirtableAsObserver
from .websites.observers.terminalasobserver import TerminalAsObserver
from .util.terminal import Terminal
import asyncio
import sys

async def main(use_terminal, use_airtable):
    playwright = await async_playwright().start()
    sites = [indeed(indeed.ANALYTICS_JOBS),
             indeed(indeed.BUSINESS_ANALYST_JOBS),
             indeed(indeed.DATA_ANALYST_JOBS),
             indeed(indeed.DATA_SCIENTIST_JOBS),
             indeed(indeed.DATA_ENGINEER_JOBS),
             wwr(wwr.DATA_JOBS),
             himalayas(himalayas.DATA_ANALYST_JOBS),
             himalayas(himalayas.BUSINESS_ANALYST_JOBS),
             himalayas(himalayas.DATA_SCIENTIST_JOBS),
             himalayas(himalayas.ANALYTICS_JOBS),
             himalayas(himalayas.DATA_ENGINEER_JOBS),
             nowb(nowb.DATA_JOBS),
             cb(cb.DAT_DATA_ANALYST_JOBS),
             cb(cb.DAT_BUSINESS_ANALYST_JOBS),
             cb(cb.DAT_ANALYTICS_JOBS),
             cb(cb.DAT_DATA_SCIENTIST_JOBS),
             cb(cb.DAT_DATA_ENGINEER_JOBS),
             cb(cb.REL_DATA_ANALYST_JOBS),
             cb(cb.REL_BUSINESS_ANALYST_JOBS),
             cb(cb.REL_ANALYTICS_JOBS),
             cb(cb.REL_DATA_SCIENTIST_JOBS),
             cb(cb.REL_DATA_ENGINEER_JOBS),
             zip(zip.DATA_ENGINEER_JOBS),
             zip(zip.DATA_SCIENTIST_JOBS),
             zip(zip.ANALYTICS_JOBS),
             zip(zip.DATA_ANALYST_JOBS),
             zip(zip.BUSINESS_ANALYST_JOBS),
             monster(monster.DATA_ANALYST_JOBS),
             monster(monster.ANALYTICS_JOBS),
             monster(monster.BUSINESS_ANALYST_JOBS),
             monster(monster.DATA_ENGINEER_JOBS),
             monster(monster.DATA_SCIENTIST_JOBS)]
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