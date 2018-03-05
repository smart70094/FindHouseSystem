#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import os
import requests
from bs4 import BeautifulSoup
import json
import re
import math
import ConditionRule


def main():
    

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
    #pages=int(math.ceil(records/30.0))
    pages=1;
    
    
    #fetch house information in each page
    house_list=[]
    for page in range(pages):
        url='https://rent.591.com.tw/home/search/rsList?is_new_list=1&type=1&kind=0&searchtype=1&region='+city_num+'&firstRow='+str(page*30)+'&totalRows='+str(records)
        content=requests.get(url,cookies=cookie,headers=headers)
        content=content.text.encode('utf-8')
        house_list.append(content)
        print '搜集資料'+str(page)+'/'+str(pages)
    

    
    
    f=open("HouseRecord",'w')
    for i,value in enumerate(house_list):
        str_json=json.loads(value)
        for j in range(30):
            house_json=str_json['data']['data'][j]
            if isVaild(house_json):
                '''
                print house_json['filename']
                print house_json['address_img_title']
                print house_json['kind_name']
                print house_json['price']
                print house_json['floorInfo']
                #print house_json['sectionname']
                print
                '''
                f.write(house_json['filename'].encode('utf-8')+',')
                f.write(house_json['address_img_title'].encode('utf-8')+',')
                f.write(house_json['kind_name'].encode('utf-8')+',')
                f.write(house_json['price'].encode('utf-8')+',')
                f.write(house_json['floorInfo'].encode('utf-8'))
                f.write('\n')
                print '目前進度'+str(i*30+j)+'/'+str(records)
                

def isVaild(house_json):
    #condition
    price_ceil=5000
    price_floor=3000
    kind_condition='套房'
    sectionname_condition='花蓮市'
    #info
    price=int(house_json['price'].replace(',',''))
    kind=house_json['kind_name'].encode('utf-8')
    sectionname=house_json['sectionname'].encode('utf-8')
    
    #proccess
    if price>=price_floor and price<=price_ceil:
        if (kind.find(kind_condition)!=-1):
            if(sectionname.find(sectionname_condition)!=-1):
                return True
    return False


#launch
main()

