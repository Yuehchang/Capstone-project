#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 15:17:33 2017

@author: changyueh
"""

import pandas as pd
import numpy as np
data = pd.read_csv('rf_2016.csv', index_col=0)

#number of company in zip california
len(data[data.state_full_name == 'california']['company'].unique())
len(data.company.unique())

#number of lead in zip 8003
len(data[(data.zip == 80003) & (data.received_month == 4)]['zip'])

#range for zip 
data.state_full_name.unique()

#create new columns 
temp_company = {}
for x in data.state_full_name.unique():
    temp = {x: len(data[data.state_full_name == x]['company'].unique())}
    temp_company.update(temp)
data['#company'] = data.state_full_name.map(temp_company)
    
data['zip_month'] = data.zip.astype(str) + data.received_month.astype(str)
data.zip_month
temp_lead = {}
for x in data.zip_month.unique():
    temp = {x: len(data[data.zip_month == x]['zip'])}
    print(temp)
    temp_lead.update(temp)
data['#lead'] = data.zip_month.map(temp_lead)

"""
categorical data 
1. type
data.type.unique() #['Supercharged Web Leads', 'Supercharged Phone Leads']\

len(data[(data.type == 'Supercharged Web Leads') & (data.zip == 12570)]['type'])
len(data[(data.type == 'Supercharged Phone Leads') & (data.zip == 12570)]['type'])

temp_type_web = {}
for x in data.zip.unique():
    temp = {x: len(data[(data.type == 'Supercharged Web Leads') & (data.zip == x)]['zip'])}
    temp_type_web.update(temp)
data['#type_web'] = data.zip.map(temp_type_web)

temp_type_phone = {}
for x in data.zip.unique():
    temp = {x: len(data[(data.type == 'Supercharged Phone Leads') & (data.zip == x)]['zip'])}
    temp_type_phone.update(temp)
data['#type_phone'] = data.zip.map(temp_type_phone)

2. source and service 
data.source.unique() #10 different source
temp_st = list(data.service_type.unique()) #35 different service some of them are not belowing to roofing service
"""

#discard unnessary columns
data.columns
useful_columns = ['state_full_name', 'city', 'zip', 'population', 'households_per_zipcode',
                  'white_population', 'black_population', 'hispanic_population',
                  'asian_population', 'hawaiian_population', 'indian_population',
                  'other_population', 'male_population', 'female_population',
                  'persons_per_household', 'avarage_house_value', 'income_per_household',
                  'elevation', 'received_month', 'cdd value', 'hdd value', 
                  'pcp value', 'tavg value', '#company', '#lead']

data = data[useful_columns]
data1 = data.drop_duplicates(subset=['zip', 'received_month'])

rename_cols = ['state', 'city', 'zip', 'population', 'hholds/zip', 'white_p', 
               'black_p', 'hispanic_p','asian_p', 'hawaiian_p', 'indian_p',
               'other_p', 'male_p', 'female_p', 'persons/hhold', 'avg_hvalue', 
               'income/hhold','elevation', 'month', 'cdd', 'hdd', 
               'pcp', 'tavg', 'num_company', 'num_lead']
data1.columns = rename_cols

#missing rate
data1.isnull().sum() / len(data1) 

data1.num_lead.value_counts().sort_values(ascending=False)
data1.num_lead.hist(bins=30)

#input missing value 'cdd value', 'hdd value', 'pcp value', 'tavg value'
miss_cols = ['cdd', 'hdd', 'pcp', 'tavg', 'state', 'num_lead']
miss_df = data1[data1.isnull().any(axis=1)][miss_cols]
miss_df.num_lead.value_counts()
data1.shape[0] - data1.dropna(axis=0).shape[0] # = drop missing value 179 rows in D.C
data1 = data1[data1.state != 'district of columbia']

data1.to_csv('rf_2016_model.csv', index=0)

#scatterplot matrix
import matplotlib.pyplot as plt
import seaborn as sns 

chart1, ax1 = plt.subplots()
sns.set(style='whitegrid', context='notebook')
sns.pairplot(data1[['cdd', 'hdd', 'pcp', 'tavg', 'num_company', 'num_lead']], size=2.5) 
plt.show()

#correlation
cor_cols = ['population', 'hholds/zip', 'white_p', 'black_p', 'hispanic_p', 'asian_p', 
            'hawaiian_p', 'indian_p', 'other_p', 'male_p', 'female_p', 'persons/hhold', 
            'avg_hvalue', 'income/hhold','elevation', 'cdd', 'hdd', 'pcp', 'tavg', 
            'num_company', 'num_lead']

chart2, ax2 = plt.subplots()
cm = np.corrcoef(data1[cor_cols].values.T)
sns.set(font_scale=0.8)
hm = sns.heatmap(cm, cbar=True, annot=True,
                 square=True, fmt='.2f',
                 annot_kws={'size': 5},
                 yticklabels=cor_cols, xticklabels=cor_cols)#heatmap = heatmap
plt.yticks(rotation=0)
plt.xticks(rotation=90)
plt.gcf().subplots_adjust(bottom=0.17)
plt.show()

#model implementation
#first model => feature selection based on correlation 
x_cols = ['white_p', 'black_p', 'hispanic_p','asian_p', 'hawaiian_p', 'indian_p',
          'other_p', 'persons/hhold', 'avg_hvalue','elevation', 'pcp', 'tavg', 
          'num_company']

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

X = data1[x_cols].values
y = data1.num_lead.values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

slr = LinearRegression()
slr.fit(X_train, y_train) 
y_train_pred = slr.predict(X_train)
y_test_pred = slr.predict(X_test)

plt.scatter(y_train_pred, y_train_pred - y_train, 
            c='blue', marker='o', label='Training data')
plt.scatter(y_test_pred, y_test_pred - y_test,
            c='lightgreen', marker='s', label='Test data')
plt.xlabel('Predicted values')
plt.ylabel('Residuals')
plt.legend(loc='upper left')
plt.hlines(y=0, xmin=-10, xmax=50, lw=2, color='red')
plt.xlim([-10, 50])
plt.show()

print('MSE train: {0:.3f}, test: {1:.3f}'.format(
        mean_squared_error(y_train, y_train_pred),
        mean_squared_error(y_test, y_test_pred)))
print('R^2 train: {0:.3f}, test: {1:.3f}'.format(
        r2_score(y_train, y_train_pred),
        r2_score(y_test, y_test_pred)))
"""
Result: no correlation between features and target; therefore, there is no predictive power
        for the models.
""" 

path = '/Users/changyueh/Desktop/UConn/17Fall/Capstone/Data/rf_2016_model.csv'
data1 = pd.read_csv(path)

#Second model => encode the number of lead to 1/0 based on #lead = 1 as 0 // #lead > 1 as 1
lead_dict = dict(data1.num_lead.value_counts())
for key, value in lead_dict.items():
    if key == 1:
        lead_dict[key] = 0
    else:
        lead_dict[key] = 1
print(lead_dict)
data1['dum_lead'] = data1.num_lead.map(lead_dict)
data1.columns

from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score

X = data1.iloc[:, 3:-2]
y = data1.iloc[:, -1]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

pipe_lr = Pipeline([('scl', StandardScaler()),
                    ('clf', LogisticRegression(penalty='l1', random_state=1))])
pipe_lr.fit(X_train, y_train)
print('Accuracy of traning: {:.3f}'.format(pipe_lr.score(X_train, y_train)))
print('Accuracy of test: {:.3f}'.format(pipe_lr.score(X_test, y_test)))

auc_list = ['accuracy', 'roc_auc']
for i in auc_list:
    scores = cross_val_score(estimator=pipe_lr,
                             X=X_train,
                             y=y_train,
                             cv=10,
                             scoring=i,
                             n_jobs=1)
    print('CV accuracy of: {0:.3f} +/- {1:.3f} [scoring condition: {2}]'.format(np.mean(scores), np.std(scores), i))

coefficients = pd.DataFrame(pipe_lr.named_steps['clf'].coef_, columns=X_train.columns)  
intercept = pd.DataFrame(pipe_lr.named_steps['clf'].intercept_, columns=['intercept'])
print(coefficients)
print(intercept)
coefs = pd.concat([intercept, coefficients], axis=1)
coefs = coefs.transpose().rename(columns={0: 'coefficients'})
coefs = coefs.rename(columns={0: 'coefficients'})

data1.to_csv('rf_2016_model_binary.csv', index=0)
"""
Results: the results is much better than linear regression. Need to try other models.
"""