"""
Author: Olin Gallet
Date: 9/2/2024

Shift from using terminal parameters to a json configuration.
-
Author: Olin Gallet
Date: 6/11/2022

Job Scraper v2 scrapes various job search websites and outputs it to
different formats.   
"""

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
from .util.configfile import ConfigFile
from typing import List
import asyncio
import sys

async def main(cfg_data:List[str]):
    playwright = await async_playwright().start()
    sites = [indeed(indeed.ANALYTICS_JOBS)]
    for site in sites:
        browser = None
        try:
            site.subscribe(TerminalAsObserver())
            browser = await playwright.firefox.launch()  
            await site.scrape(browser)
            await browser.close()
        except Exception as e:
            Terminal.display_website_error(site.get_url(), e.message)
            if browser is not None:
                await browser.close()
    await playwright.stop()

def execute():
    """
    Attempts to execute the jobscraper with the provided configuration file location.
    """
    if len(sys.argv) != 2:
        Terminal.display_usage_help()
    else:
        cfg = ConfigFile(sys.argv[1])
        if cfg.exists():
            try:
                cfg_data = cfg.parse()
                Terminal.display_attempting_scrape(sys.argv[1], cfg_data["position"], \
                                                   cfg_data["location"], \
                                                   cfg_data["engine"], cfg_data["output"])
                asyncio.run(main(cfg_data))
            except Exception as e:
                Terminal.display_parse_error(sys.argv[1], e.message)
        else:
            Terminal.display_configuration_not_found_error(sys.argv[1], e.message)
             
    
if __name__ == '__main__':
    execute()