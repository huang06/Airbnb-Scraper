# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 06:37:42 2017

@author: race020
"""

import requests
from bs4 import BeautifulSoup
import pandas
import time
import csv


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

res = requests.get('https://www.airbnb.com/users/show/29169973',headers=headers)
soup = BeautifulSoup(res.text,"lxml")
print(soup)

"""
scrape links from reviewers as host
"""   
link =[]

for x in soup.findAll('div',{'class':'reviews_section as_guest space-top-3'}):
    for y in x.findAll('div',{'class':'col-md-2 col-sm-12'}):
        for z in y.findAll('a',{'class':'text-muted','rel':"nofollow"}):
                print(z['href'])
                link.append(z['href'])

# Create a variable of the value of the columns
columns = {'links_from_host': link}

# Create a dataframe from the columns variable
user_profile = pd.DataFrame(columns)

