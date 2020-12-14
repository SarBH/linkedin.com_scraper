# linkedin.com_scraper
Scrape linkedin for profiles matching a specific search, and parse their career history into a csv

This repository contains two main scritps:

## part 1: Login and Scrape
This script iterates through a search on linkein.com, and downloads the HTMLs of the profiles on the search results.
For example, if I wanted all profiles associated with "Intel Corporation" I would make that search on linkedin.com and copy the URL. Then I run this script with that URL and indicate how many results I want to see.
All functions are documented. 

### How to run?
Enter your linkedin username and password on lines 121-122. Enter the URL and the number of pages you want to scrape on line 129.


## part 2: parse and Write
This script parses the HTMLs saved in search for all the companies that the profile owner has worked for in his/her career.
It does that by looking for the string “companyName” in the HTML file for a profile. Using only the relevant appearances and preventing repeats, it writes the company names to a csv.

### How to run?
After running part 1 script, the HTMLs were saved to a new ./profiles folder in the same directory as the part 1 script. Assuming you didnt change any directory, you can simply run this script.
