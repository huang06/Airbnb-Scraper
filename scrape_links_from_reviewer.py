# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 15:25:00 2017

@author: race020
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd


# https://www.airbnb.com.tw/users/review_page/9639741?page=1&role=guest
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

res = requests.get('https://www.airbnb.com.tw/users/review_page/9639741?page=1&role=guest',headers=headers)
soup = BeautifulSoup(res.text,"lxml")
print(soup)

"""
scrape links from reviewers as host
"""   
link =[]
import re
# {'class':'text-muted','rel':"nofollow"}
for z in soup.findAll('a',{"rel":re.compile("nofollow")}):
    print(z['href'])
    link.append(z['href'])

# Create a variable of the value of the columns
columns = {'links_from_host': link}

# Create a dataframe from the columns variable
user_profile = pd.DataFrame(columns)
user_profile['links_from_host'] = \
            user_profile['links_from_host'].map(lambda x: x.strip('\\\" /users/show/ '))
print(user_profile['links_from_host'])
# Print the URL list of hosts on which the user has comment
print('https://www.airbnb.com.tw/users/show/'+user_profile['links_from_host'])
