#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 17:49:26 2017

@author: changyueh
"""
import pandas as pd
#list of all states in US
state_names = ['Connecticut', 'Delaware', 'Maine', 'Maryland', 'Massachusetts', 'New Hampshire', 'Rhode Island', 'Vermont', 'New Jersey', 'New York', 'Pennsylvania', 
              'Illinois', 'Indiana', 'Kentucky', 'Missouri', 'Ohio', 'Tennessee', 'West Virginia',  
              'Iowa', 'Michigan', 'Minnesota', 'Wisconsin',
              'Idaho', 'Oregon', 'Washington',
              'Arkansas', 'Kansas', 'Louisiana', 'Mississippi', 'Oklahoma', 'Texas',
              'Alabama', 'Florida', 'Georgia', 'North Carolina', 'South Carolina', 'Virginia',  
              'Arizona', 'Colorado',  'New Mexico', 'Utah', 
              'California', 'Nevada',
              'Nebraska', 'North Dakota', 'South Dakota', 'Montana',  'Wyoming',
              'Alaska', 'Hawaii', 'District of Columbia'] 
               
               

#List of all regional divisions: the first 6 states in "state_names" is 'New England'              
regions = ['Northeast']*11 + ['Central']*7 + ['East North Central']*4 + ['Northwest']*3 + ['South']*6 + ['Southeast']*6 + ['Southwest']*4 + ['West']*2 + ['West North Central']*5 + ['Other']*3
        
#Create Dataframe which column is regional division and index is states' name
state_division = pd.DataFrame({'region': regions}, index=state_names)

#Join DF'state_division' to US_data
US_data1 = pd.merge(US_data1, state_division, left_on='state_full_name', right_index=True)

US_data1 = US_data1.drop('country', axis=1)

US_data1.to_csv('US_data1.csv',index=False)
