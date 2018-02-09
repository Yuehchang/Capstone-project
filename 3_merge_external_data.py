#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 12:17:00 2017

@author: changyueh
"""
import pandas as pd
state_names = ['Connecticut', 'Delaware', 'Maine', 'Maryland', 'Massachusetts', 'New Hampshire',
	      'Rhode Island', 'Vermont', 'New Jersey', 'New York', 'Pennsylvania', 
              'Illinois', 'Indiana', 'Kentucky', 'Missouri', 'Ohio', 'Tennessee', 'West Virginia',  
              'Iowa', 'Michigan', 'Minnesota', 'Wisconsin',
              'Idaho', 'Oregon', 'Washington',
              'Arkansas', 'Kansas', 'Louisiana', 'Mississippi', 'Oklahoma', 'Texas',
              'Alabama', 'Florida', 'Georgia', 'North Carolina', 'South Carolina', 'Virginia',  
              'Arizona', 'Colorado',  'New Mexico', 'Utah', 
              'California', 'Nevada',
              'Nebraska', 'North Dakota', 'South Dakota', 'Montana',  'Wyoming',
              'Alaska'] 
columns = ['Date', 'Value', 'Anomaly', 'State']
folder_names = ['ed_cdd', 'ed_hdd', 'ed_pcp', 'ed_tavg']

for j in folder_names:
    data_merge = pd.DataFrame(columns=columns)
    for i in state_names:
        path_read = './Capstone/Data/{1}/{0}.csv'.format(i, j)
        temp = pd.read_csv(path_read, index_col=0)
        data_merge = data_merge.append(temp, ignore_index=True)
        data_merge
        print ('the state: {} is merged into table'.format(i))
    if_statement = len(data_merge.State.unique()) == len(state_names)
    print ('Table {1}.csv is sccussfully merged: {0}'.format(if_statement, j))
    save_name = '{}.csv'.format(j)
    data_merge.to_csv(r'./Capstone/Data/{}'.format(save_name), index=False) 
    print ('Table {} has been merged'.format(save_name))
    


