from selenium import webdriver
from bs4 import BeautifulSoup
import re
import time
import requests
import csv
import os
import io
import pickle
import random
import sys


def login_linkedin(username, password):
    """ Given a username and a password for a linkedin account, open a browser and log in to linkedin."""
    browser = webdriver.Chrome("chromedriver.exe")
    #Open login page
    browser.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')
    #Enter login info:
    elementID = browser.find_element_by_id('username')
    elementID.send_keys(username)
    elementID = browser.find_element_by_id('password')
    elementID.send_keys(password)
    elementID.submit()
    
    return browser


def get_urls_to_save():
    """ retrieve existing pickled list of urls. If the list does not exist (if its the first time running the file), 
    start a new list"""
    if os.path.exists("profile_urls_to_save.txt"):
        with open("profile_urls_to_save.txt", "rb") as fp:
            profile_urls_to_save = pickle.load(fp)
            print("loaded profile_urls_to_save from file. It contains", len(profile_urls_to_save), "listings pending saving their html to disk")
    else:
        profile_urls_to_save = list()
        print("profile_urls_to_save list was not found in the cwd. Creating new list")

    return profile_urls_to_save


def get_urls_to_scrape():
    """ retrieve existing pickled list of urls. If the list does not exist (if its the first time running the file), 
    start a new list"""
    if os.path.exists("profile_urls_to_scrape.txt"):
        with open("profile_urls_to_scrape.txt", "rb") as fp:
            profile_urls_to_scrape = pickle.load(fp)
            print("loaded profile_urls_to_scrape from file. It contains", len(profile_urls_to_scrape), "listings that have already been saved as htmls and are pending scraping.")
    else:
        profile_urls_to_scrape = list()
        print("profile_urls_to_scrape set was not found in the cwd. Creating new set")

    return profile_urls_to_scrape



def scrape_profile_urls_to_save(browser, url,start_page_num, end_page_num):
    """ Iterate throught the search results for the search indicated by "url". Scrape for the profile_urls in all the search result pages.
    This method also saves the HTML for the search result pages, since it is a low cost operation and it could be useful in the future. 
    (Especially because we dont want to make any unnecesary requests to linkedin.com)
    """
    for list_page in range(start_page_num, end_page_num): # for each page containing a list of people
        print ('Scraping page', str(list_page))
        page_link=url+'&page='+str(list_page) # make the page url for each pag
        browser.get(page_link)
        list_html = browser.page_source

        with io.open("list_pages/page" + str(list_page) + "list.html" , "w", encoding="utf-8") as html_file:
                    html_file.write(list_html)
                    html_file.close()

        list_soup = BeautifulSoup(list_html,'html') # parse the html using BS so we can get the links to the specific profiles' sites
        profile_tags = list_soup.findAll('a', {'class':'app-aware-link ember-view search-result__result-link'}) # get a list of all the <a> tags that contain the url for each profile

        # add all of the profile urls found on the page to the "profile_urls_to_save" queue
        for profile_idx, profile in enumerate(profile_tags):
            print("Processing profile #", profile_idx, "from page", str(list_page))
            profile_url = profile.get("href") # complete the url since only the tail of it is given
            print("...", profile_url)
            # make sure its a new profile that we havent seen before
            if profile_url in profile_urls_to_save or profile_url in profile_urls_to_scrape:
                print("profile #", profile_idx, "from page", str(list_page), "is already seen. Skipping")
                continue
            if "linkedin.com/in/" in profile_url:
                profile_urls_to_save.append(profile_url)

    # after we've collected all profile urls that we need, update the pickled list on file
    print("collected", len(profile_urls_to_save), "profile urls to save as html")       

    with open("profile_urls_to_save.txt", "wb") as fp:
        pickle.dump(profile_urls_to_save, fp)

    return profile_urls_to_save



def save_source_html(browser, profile_url, profile_idx):
    if "linkedin.com/in/" in profile_url:
        browser.get(profile_url)
        profile_html = None

        # use html size as a shortcut to ensure that the html is an actual profile, and not a failure to open the page due to capcha or network error
        while sys.getsizeof(profile_html) < 200000:
            profile_html = browser.page_source
            time.sleep(random.random()*4)

        # as per the deliverables, save the html for each profile
        current_dir = os.path.dirname(os.path.realpath(__file__))
        if not os.path.exists(os.path.join(current_dir, str("profiles"))):
            os.makedirs(os.path.join(current_dir, str("profiles")))            
        with io.open("profiles/" + "/profile_" + profile_url.rsplit('/', 1)[-1] + ".html" , "w", encoding="utf-8") as html_file:
            html_file.write(profile_html)
            html_file.close()
        print("Saved HTML for profile:", profile_url.rsplit('/', 1)[-1])
            
    

if __name__ == "__main__":

    username = "dummyemail@gmail.com"
    password = "dummypassword"
    browser = login_linkedin(username, password)
    print("Browser opened and user has logged in")

    # retrieve lists of urls 
    profile_urls_to_save = get_urls_to_save() #these are the urls that we have seen but not saved their html yet
    profile_urls_to_scrape = get_urls_to_scrape() # these are the urls that we already saved their html, but havent scraped yet
    # profile_urls_to_save = scrape_profile_urls_to_save(browser, 'https://www.linkedin.com/search/results/people/?currentCompany=%5B%221053%22%2C%22727974%22%5D&origin=COMPANY_PAGE_CANNED_SEARCH', 1, 100)

    qty_to_save = len(profile_urls_to_save)
    qty_to_scrape = len(profile_urls_to_scrape)
    print(f"---Loaded {qty_to_save} profiles pending to be saved as htmls, and {qty_to_scrape} profiles that we already have htmls for and must be scraped")
    
    idx = 0
    while(len(profile_urls_to_save)) > 0: # get html for all of the profile_urls we retrieved
        url = profile_urls_to_save.pop(0)
        save_source_html(browser, url, idx)
        profile_urls_to_scrape.append(url)
        time.sleep(random.randint(0,4))
        idx += 1
        print("completed scrapes:", idx)
        # update the queues
        with open("profile_urls_to_save.txt", "wb") as fp:
            pickle.dump(profile_urls_to_save, fp)
        with open("profile_urls_to_scrape.txt", "wb") as fp:
            pickle.dump(profile_urls_to_scrape, fp)

    qty_to_save = len(profile_urls_to_save)
    qty_to_scrape = len(profile_urls_to_scrape)
    print(f"---Finished with {qty_to_save} profiles pending to be saved as htmls, and {qty_to_scrape} profiles that we already have htmls for and must be scraped")
    
