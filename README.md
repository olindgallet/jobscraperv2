# Job Scraper, Version 2
Scraper for job sites done with Python and the Playwright library.

### Do Note That This Project is Incomplete!
I will be testing this soon on a virtual machine.  My programming computer uses ElementaryOS and is not officially supported by Playwright.  So I will be setting up a VM and running some tests.  Use the code at your own risk.

### Current Basic Installation (on Linux machines)
0.  Open the terminal and go to the folder where you want to install the program.
1.  ```gh repo clone olindgallet/jobscraperv2``` to download the repository.
2.  ```pip3 -m install requirements.txt to``` download dependancies.
3.  ```playwright install``` to install browsers for Playwright.
4.  ```python3 jobscraperv2.py -t``` to run the program and output to terminal.

### Sending Data to Airtable (on Linux machines)
0.  Create an Airtable (http://www.airtable.com) base, then an Airtable field with the following fields: job_company, job_title, job_description, job_link, job_date.
1.  Open the terminal and type in ```nano ~/.bashrc```
2.  Add in the following three lines at the end of the file: export AIRTABLE_BASE_KEY={your key}, export AIRTABLE_NAME={table name}, and export AIRTABLE_API_KEY={your api key}.  The information can be found in your base settings of Airtable.
3.  ```.source ~/.bashrc``` to refresh the bash environment.
4.  ```python3 jobscraperv2.py -t -a``` to run the program and output to terminal.
