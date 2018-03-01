#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import requests
from bs4 import BeautifulSoup
import json
import re
import math

#fetch web information that it's about code of city
url='https://rent.591.com.tw/?kind=0&region=8'
headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',}
content=requests.get(url,headers=headers).text.encode('utf-8')

#fetch city html
datas_soup=BeautifulSoup(content, "html.parser")
targets_soup=datas_soup.find_all('p',{'class':'clearfix changRegion'})

city_soup=targets_soup[0].find_all('a')

city_num='23'
cookie={
    'urlJumpIp':city_num,
    }

url='https://rent.591.com.tw/home/search/rsList?is_new_list=1&type=1&kind=0&searchtype=1&region='+city_num
content=requests.get(url,cookies=cookie,headers=headers)
content=content.text.encode('utf-8')
data_json=json.loads(content)
records= int(data_json['records'])
pages=int(math.ceil(records/30.0))

#fetch house information in each page
house_json=[]
for page in range(pages):
    url='https://rent.591.com.tw/home/search/rsList?is_new_list=1&type=1&kind=0&searchtype=1&region='+city_num+'&firstRow='+str(page*30)+'&totalRows='+str(records)
    content=requests.get(url,cookies=cookie,headers=headers)
    content=content.text.encode('utf-8')
    data_json=json.loads(content)
    house_json.append(data_json['data']['data'])
    
for page in range(0,pages):
    for i in range(0,29):
        print 'Title:'+house_json[int(i)]['address_img_title']+'\n'
        
    
    
    



