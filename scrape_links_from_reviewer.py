# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 15:25:00 2017
@author: race020
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

"""
Test
"""
a = [0, 1, 2, 3]
type(a)
user_list=user_list.set_index("user_id")
type(user_list.loc[user_list['user_id'] == 113304043]['host_id'])
user_list.loc[113304043, "host_id"] = user_profile['links_from_host'].values.tolist()
             
reviews_raw['reviewer_id'].head(10).values.tolist()  
        
"""
Create a list of user_id
"""
user_list = pd.DataFrame(columns=['user_id','host_id'])

user_list['user_id'] = reviews_raw['reviewer_id'].head(100).values.tolist() 
user_list=user_list.set_index("user_id")

"""
Scrape links from user web
"""
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

page = 1
for index, row in user_list.iterrows():
    try:
        print('Following content of URL will be scraped : ')
        print('https://www.airbnb.com.tw/users/review_page/'+str(index)+'?page='+str(page)+'&role=guest')
        #page+=1
        res = requests.get('https://www.airbnb.com.tw/users/review_page/'+str(index)+'?page='+str(page)+'&role=guest',headers=headers)
        soup = BeautifulSoup(res.text,"lxml")
        print(soup)
        """
        scrape links from reviewers as host
        """
        links =[]
        for z in soup.findAll('a',{"rel":re.compile("nofollow")}):
            print(z['href'])
            links.append(z['href'])  
        # Create a variable of the value of the columns
        columns = {'links_from_host': links}
        
        # Create a dataframe from the columns variable
        user_profile = pd.DataFrame(columns)
        user_profile['links_from_host'] = \
                    user_profile['links_from_host'].map(lambda x: x.strip('\\\" /users/show/ '))
        print(user_profile['links_from_host']) 
        # Print the URL list of hosts on which the user has comment
        print('https://www.airbnb.com.tw/users/show/'+user_profile['links_from_host'])
        # Store the URL list to user_profile
        user_list.loc[index, "host_id"] = user_profile['links_from_host'].values.tolist()
    except:
        continue
