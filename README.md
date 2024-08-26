# Job Scraper, Version 2
A scraper for job sites done with Python and the Playwright library.

# In the Works: Job Scraper Update 8/26/2024
After receiving kind words and support, I've decided I want to update the scraper.  Here are the goals
hoping to be reached around Labor Day:

1.  Transition from command line parameters to JSON configurations.  Things that should change like
location and job position are hard-coded, which makes it difficult for different needs to be met.
2.  Include support for exporting to CSVs.  Credit to user lukegeel101 for the suggestion / code.
3.  Get as many of the website scrapers working as possible.

Right now the goal is to have it pull raw data from the sites.  No sort of processing and display will be added in this program at least.

### Why v2?  Is there an earlier version?
The earlier version uses Selenium and has time delays to account for Javascript loads and rendering.  This version uses Playwright and properly "waits" for rendering rather than force a delay.  The program as a whole now runs faster; those unused seconds of waiting for rendering add up!  

### As of now, this project is "complete".
By that I mean the project does what I want it to do to satisfaction.  It scrapes 1000+ jobs and deposits the data into an Airtable, after which I can remove duplicate data and process the information as needed.  You will need to modify the variables and function calls if you want to job scrape a different niche.  If you would like to scrape a larger amount of data (and have the computer power to do so), the framework is laid out for parallel execution.

### Known Bugs
- ZipRecruiter works inconsistently.  On my personal PC, I'm able to scrape it just fine as I assume it is using the cookies to get past the window that pops.  However, on the virtual machine, it has issues.  I assume that the login window "pops up" on the headless browser, and while I did try to login on that browser, the login persistence isn't stopping that window from popping up.  So for now, the code to scrape ZipRecruiter is there, but it's not being used.
- Dice also works inconsistently.  During some scrapes, it has crashed the instance running the code.  After running the website through gtmetrix and seeing an F grade, I suspect that the website is so poorly optimized it needs more resources than necessary to be scraped.  However, I've found that the job quality on the site is poor, so I don't use it.
- Hitmarker is usable, but because of the high job requirements and the poor semantic design of the website, it can be hard to scrape.  If you do want to scrape it, you'll likely need to modify some of the code.

### Current Basic Installation:
0.  Go to the folder where you want to download the files. 
1.  ```gh repo clone olindgallet/jobscraperv2``` to download the repository.
2.  ```cd jobscraperv2``` to go into the downloaded repository.
2.  ```pip3 -m install requirements.txt``` to download dependancies.
3.  ```playwright install``` to install browsers for Playwright.
4.  ```python3 jobscraperv2.py -t``` to run the program and output to terminal.

### Sending Data to Airtable (on Linux machines)
0.  Create an Airtable (http://www.airtable.com) base, then an Airtable with the following fields: job_company, job_title, job_description, job_link, job_date.
1.  Move to the ```jobscraperv2/src``` directory and type in ```touch .env``` to create the env file.  Open it up in your editor of choice.
2.  Add in the following three lines: export AIRTABLE_BASE_KEY={your key}, export AIRTABLE_NAME={table name}, and export AIRTABLE_API_KEY={your api key}.  The information can be found in your base settings of Airtable.  As Airtable has moved to an IAM system, you also need to set up an identity with read priviledges through the Airtable interface.
3.  Move out of the src directory by typing ```cd ..```.
4.  ```python3 jobscraperv2.py -t -a``` to run the program and output to terminal and Airtable.

![Airtable view of example data](https://github.com/olindgallet/jobscraperv2/blob/master/AirtableReview.png)
Note that through Airtable you can implement handy filters (on the left side) to further analyze data.

### Tips for Automating the Scraper
- I use an a1.large ec2 instance for the automation.  It was selected as it has up to 10 Gbps bandwidth for network transactions while having enough processing power to scrape the data.  At around .20 an hour, monthly costs are 8 dollars to run the instance two hours each weeknight.
- Optimize run costs with the Amazon instance scheduler.  There's no need to run this 24 hours a day.
- Cron scheduler is enough for basic automation.  In addition to the job scraper, I also run a bot that takes the scrape log (it's just the output redirected to a text file) and pushes it to a Discord channel.  It's handy for debugging errors.

### Tips for Customizing the Scraper
- Look in ```src/__main__.py``` for code to select the scrapers used and the variables containing the URLs of the sites.  Change as needed.
- If you want to select a different niche, add a variable in each scraper class.  They are at the beginning of the code, are fully capitalized, and assigned the url of the target webpage.
- If you want to implement a scraping algorithm for a website, place the code in ```src/jobscraperv2/websites```.  Have it implement the ```websiteinterface.py``` class and provide a scraping method.  Use the existing websites as a guide.
- If you want to send the data to a recipient besides Airtable and the terminal, you need to implement an observer in ```src/jobscraperv2/websites/observers```.  Have the observer implement the ```observerinterface.py``` class and provide a notify method that processes the received data.  Use the existing observers as a guide.

### Project Analysis
I'll be doing a writeup on LinkedIn.  It'll be over the next few weeks so I'll add the links here once I get done.
