# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 15:25:00 2017
@author: Dormitory
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

"""
目前用不到的Code
"""
a = [0, 1, 2, 3]
type(a)
type(user_list.loc[user_list['user_id'] == 113304043]['host_id'])
user_list.loc[113304043, "host_id"] = user_profile['links_from_host'].values.tolist()
# 增加 value 到現有的 list 用 extend ; 增加 list 到現有的 list 用 append
user_list.loc[index, 'host_id'].extend(user_profile['links_from_host'].values)
# 找目標 index 在 DataFrame 裡排序位置
user_list.index.get_loc(index)

"""
建立user_id清單，並把user_id設為index
    移除掉重複的user_id : 646717 -> 570681
"""
reviews_raw = pd.DataFrame(pd.read_csv('C:/Users/race020/Desktop/repository/reviews.csv'))

df = pd.DataFrame(columns=['user_id','host_id','count'])
df['user_id'] = reviews_raw['reviewer_id'].values.tolist() 
df = df.drop_duplicates()
df=df.set_index("user_id")
# 預設 host_id 為 empty list
df['host_id'] = [[] for _ in range(len(df))]
# 預設 count 為 int
df['count'] = [0 for _ in range(len(df))]
df = df.sort_index()

"""
選適合的 copy
"""
user_list = df.iloc[10001:20000].copy()

#user_list = df.iloc[0:50000].copy()
#user_list = df.iloc[50001:100000].copy()
#user_list = df.iloc[100001:150000].copy()
#user_list = df.iloc[150001:200000].copy()
#print(df.index.get_loc(220493))


"""
Scraper Go!
"""
tStart = time.time()#計時開始
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

for index, row in user_list.iterrows():
  #因為 index 從 0 開始，所以 current + 1 
  current = user_list.index.get_loc(index)+1
  print(' 進度:'+ str(current) + ' / ' + str(len(user_list)))                                   
  if ( current%500==0 ) :
      user_list.to_csv(str(current)+'.csv',index=True)    
  try:
      for page in range(1,10): #比起設do-while還能控制流程
            """
            爬網頁內容
            """
            #print('Following content of URL will be scraped : ')
            #print('https://www.airbnb.com.tw/users/review_page/'+str(index)+'?page='+str(page)+'&role=guest')
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
            #print(user_profile['links_from_host'])
            #print('https://www.airbnb.com.tw/users/show/'+user_profile['links_from_host'])
            
            #print(' 進度:'+ str(user_list.index.get_loc(index)) + ' / ' + str(len(user_list)))
            #print('目前第'+str(page)+'頁 '+'user_profile的長度:'+str(len(user_profile))) 
            
            #離開page-loop條件
            if (len(user_profile)==0):
                break
            
            #host_id 匯入
            #print('要加入的list'+str(user_profile['links_from_host'].values.tolist()))
            user_list.loc[index, 'host_id'].extend(user_profile['links_from_host'].values)            
            user_list.loc[index, 'count'] += len(user_profile)
  
  except (KeyboardInterrupt, SystemExit):
      print('xxxxxxxxxxxxxxxxxx')
      user_list.to_csv('total.csv',index=True)
      raise
user_list.to_csv('total.csv',index=True)      
tEnd = time.time()#計時結束
print( "It cost %f sec" % (tEnd - tStart) )#會自動做近位
print( tEnd - tStart )#原型長這樣
