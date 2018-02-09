#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 11:59:14 2017

@author: changyueh
"""

import pandas as pd
import time
import os
from urllib.request import urlopen
from bs4 import BeautifulSoup

month_ls = ['01','02','03','04','05','06','07','08','09','10','11','12']
state_ls = ['50','01','02','03','04','05','06','07','08','09']
# state_ls = []
state_ls.extend(list(map(str,list(range(10,49)))))
    

def get_external(varname):
   for j in state_ls:
    data_all = pd.DataFrame()
    for i in month_ls:
        url = "https://www.ncdc.noaa.gov/cag/time-series/us/{1}/00/{2}/1/{0}/2007-2017.csv?base_prd=true&begbaseyear=1901&endbaseyear=2000".format(i,j, varname)
        html = urlopen(url)
        time.sleep(1)
        bsObj = BeautifulSoup(html,'lxml')
        ls = bsObj.get_text().split('\n')
        name = ls[0].split(',')[0]
        var_name = ls[4].split(',')
        table = list()
        for k in ls[5:(-1)]:
            temp = k.split(',')
            temp.append(name)
            table.append(temp)
        var_name.append('State')
        data = pd.DataFrame(table,columns=var_name)
        data_all = pd.concat([data_all,data])
        print('the state:{0} the month:{1}'.format(name,i))
    save_path = name+r'.csv'
    
    dest = os.path.join(r'/Users/changyueh/Desktop/UConn/17Fall/Capstone/Data/ed_{}'.format(varname))
    if not os.path.exists(dest):
        os.makedirs(dest)
    
    data_all.to_csv(os.path.join(dest, r'{}'.format(save_path)), index=False)
    print('the state: {0} crawl finish'.format(name)) 

get_external('tavg')
get_external('pcp')
get_external('hdd')
get_external('cdd')
get_external('tmin')
