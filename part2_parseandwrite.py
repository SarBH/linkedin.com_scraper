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
import io
import codecs


def parse_employment_history(profile_html):
    """ This function looks for the string “companyName” in the HTML file for a profile. 
    The first 7 appearances of that string (including quotes) are to be discarded. 
    Starting from the 8th appearance, the text within quotes that appears immediately after “companyName” 
    are the companies the profile owner worked for during their careers.
    Save into a set to avoid repeats, and write the elements of the set to a csv.
    """
    company_names = set()
    match_idxs = [m.end() for m in re.finditer('"companyName"', profile_html)]
    match_idxs = match_idxs[8:] # discard first 7 entries because they dont contain the company names we are looking for
    start_idxs = [match + 2 for match in match_idxs] # skip the two characters (:") after "companyName", the target string beings there
    # look for the end of the quoted text immidiately after "companyName", as it contains the string we want
    end_idxs = []
    for start in start_idxs:
        end_idxs.append(profile_html.index('"', start, start+200))
    # 
    for start, end in zip(start_idxs, end_idxs):
        company_names.add(profile_html[start:end])
    
    writer.writerow(company_names)



if __name__ == "__main__":
        
    csv_file=open('company_history.csv','a',encoding='utf8') # creates and opens a file called company_history.csv to place the <comp1>,<comp2> etc one person's history per line
    writer=csv.writer(csv_file,delimiter=",", lineterminator='\n') # create a csv writer to write the company history for each person
    current_dir = os.path.dirname(os.path.realpath(__file__))
    # iterates through every html file saved on the ./profiles directory, and opens them one by one.
    for unscraped_profile in os.listdir("profiles"):
        html_string = codecs.open(str("profiles/"+unscraped_profile), "r", "utf-8")
        html_string = html_string.read()
        # run the parsing function
        parse_employment_history(html_string)
        # Lastly, move the HTML file to another folder.
        if not os.path.exists(os.path.join(current_dir, str("scraped"))):
            os.makedirs(os.path.join(current_dir, str("scraped")))
        os.rename(str("profiles/"+unscraped_profile), str("scraped/"+unscraped_profile))
    
    csv_file.close()


    