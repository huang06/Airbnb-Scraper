# -*- coding: utf-8 -*-
"""
Created on Sat Dec 24 21:00:47 2016

@author: Dormitory
"""

import requests
from bs4 import BeautifulSoup
import pandas
import time
import csv



headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
count = 1
df=pandas.read_csv("C:/Users/Dormitory/Desktop/id.csv",converters={"id":int})

for index, row in df.iterrows():
    time.sleep(5)
    thefile = open('C:/Users/Dormitory/Desktop/test.txt', 'a+')
    #print(str(row['id']))   
    res = requests.get('https://www.airbnb.com/users/show/'+str(row['id']),headers=headers)
    soup = BeautifulSoup(res.text,"lxml")
    #<div class="h5 space-top-2">
    #<a href="/s/洛杉磯--加州" class="link-reset">洛杉磯, 加州, 美國</a>
    for x in soup.findAll('div',{'class':'h5 space-top-2'}):
        for link in x.findAll('a',{'class':'link-reset'}):
            print(count)
            count+=1
            #print(row['id'])
            #print(link.text)
            a = link.text
            a = a.replace(",", "-")
            a = a.replace(" ","")
            thefile.write("%s " % row['id'])
            thefile.write("%s\n" % a.encode('utf8'))
    thefile.close()
            
