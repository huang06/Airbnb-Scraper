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
測試用
"""
a = [0, 1, 2, 3]
type(a)
user_list=user_list.set_index("user_id")
type(user_list.loc[user_list['user_id'] == 113304043]['host_id'])
        
"""
建立user_id
"""
reviews_raw = pd.DataFrame(pd.read_csv('C:/Users/Dormitory/Desktop/reviews.csv'))

df = pd.DataFrame(columns=['user_id','host_id','count'])
df['user_id'] = reviews_raw['reviewer_id'].values.tolist() 
df=df.set_index("user_id")
df['host_id'] = [[] for _ in range(len(df))]
df['count'] = [0 for _ in range(len(df))]
user_list = df.copy().head(10)

"""
準備Scraper
"""
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
for index, row in user_list.iterrows():
  for page in range(1,100): #比起設do-while還能控制流程
    try:
            """
            爬網頁內容
            """
            print('Following content of URL will be scraped : ')
            print('https://www.airbnb.com.tw/users/review_page/'+str(index)+'?page='+str(page)+'&role=guest')
            res = requests.get('https://www.airbnb.com.tw/users/review_page/'+str(index)+'?page='+str(page)+'&role=guest',headers=headers)
            soup = BeautifulSoup(res.text,"lxml")
            #print(soup)
            
            """
            拿出host_id
            """
            links =[]
            for z in soup.findAll('a',{"rel":re.compile("nofollow")}):
                #print(z['href'])
                links.append(z['href'])  
            # Create a variable of the value of the columns
            columns = {'links_from_host': links}
            
            # Create a dataframe from the columns variable
            user_profile = pd.DataFrame(columns)
            user_profile['links_from_host'] = \
                        user_profile['links_from_host'].map(lambda x: x.strip('\\\" /users/show/ '))
            print(user_profile['links_from_host'])
            #print('https://www.airbnb.com.tw/users/show/'+user_profile['links_from_host'])
            print('目前第'+str(page)+'頁 '+'user_profile的長度:'+str(len(user_profile))) 
            #離開page-loop條件
            if (len(user_profile)==0):
                break
            print('要加入的list'+str(user_profile['links_from_host'].values.tolist()))
            user_list.loc[index, 'host_id'] += user_profile['links_from_host'].values.tolist()          
    except:
        print('xxxxxxxxxxxxxxxxxx')
        page+=1
        #continue
