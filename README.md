# BIA660 Extra Credit LinkedIn Scraper

Scrape linkedin for profiles matching a specific search, and parse their career history into a csv

# How to run?
- edit the main() method on part1_loginandscrape.py to include your username, password
and the link for the search you would like to scrape (in my case, one of the URLs was
“​https://www.linkedin.com/search/results/people/?keywords=intel&origin=SWITCH_SEARCH_V
ERTICAL​”)
- run part2_parseandwrite.py.

The code will output 2 lists saved as pickles, and a company_history.csv file.

This repository contains two main scritps:
## part 1: Login and Scrape
This script iterates through a search on linkein.com, and downloads the HTMLs of the profiles on the search results.
For example, if I wanted all profiles associated with "Intel Corporation" I would make that search on linkedin.com and copy the URL. Then I run this script with that URL and indicate how many results I want to see.
This file performs the following tasks:
● Use selenium browser to open and login to linkedin.com
● Navigates to the search that we are interested in. In this case, people who worked for
  Intel at some point in their careers.
● Saves the html for the profiles to disk.

### Implementation details of the scraper
The implementation consists of keeping two queues: one for the URLs of the profiles to scrape,
and another for those profiles that we already stored HTML files, but haven't yet parsed.
1. open the search results and scrape the URLs of the profiles for all of the pages on the
range we selected when running main()
2. Store the URLs as strings in a list. We pickle that list and store in disk in case the code
crashes, we don't have to repeat work.
3. One by one, dequeue the URLs from the queue, use Selenium to open the profile, and
store the HTML to disk.
4. Enqueue the already saved URL string to another queue, for the profiles that we haven't
scraped for employment history.

The actual parsing for employment history happens in the file for part2. The benefits of
separating into two files in this way is that the second part won't have to enter the web at all, as
it can work directly from the saved HTMLs. Therefore, I can run the html scraper during the time
that I’m blocked out of LinkeinIn.com if that ever happens.


## part 2: parse and Write
This script parses the HTMLs saved in search for all the companies that the profile owner has worked for in his/her career.
It does that by looking for the string “companyName” in the HTML file for a profile. Using only the relevant appearances and preventing repeats, it writes the company names to a csv.
Specifically:
1. iterates through every html file I saved on the ./profiles directory, and opens them one by
one.
2. it looks for the string “companyName”. The first 7 appearances of that string
(including quotes) are to be discarded. Starting from the 8th appearance, we look at the
text within quotes that appears immediately after “companyName”.
3. I save the company names into a set to avoid writing a company twice when the profile
contains a promotion or a change of title within the same company (since we're only
interested in naming the companies the person worked for).
4. I use csv writer to write the elements of the set to a csv.
5. Lastly I move the HTML file to another folder. I do this until I have parsed all of the
HTMLs in the ./profiles directory.

