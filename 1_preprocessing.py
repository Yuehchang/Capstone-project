from __future__ import division
import pandas as pd

dtype_dic= {'id': str, 'zip' : str}
lead_data=pd.read_csv(r'UCONN Updated 10 Years.csv',dtype=dtype_dic)
lead_data.head()

pd.Series(lead_data.columns)

lead_x=['id','zip','type','source','association','service_type','received_time','company','status','price',
        'campaign','is_mobile','call_status']
#removed address(literal descriptions), sent_time(same as received_time),landing_page, contact_page, previous_page(all URL info),
#inbound_number,duration(call duration), job_sold(most missing)

lead_data1=lead_data[lead_x]
lead_data1

#missing rate calculatino
def missing_rate(data,name):
    print (name+' missing rate')
    for i in data.columns:
        null_num=(data[i].isnull()).sum()
        if null_num !=0:
            print (i+':         ' '%.4f%%' % (null_num/len(data)*100))
missing_rate(lead_data1,'lead_data1')

dtype_dic= {'zipcode.zip': str, 'zipcode.area_code': str,'zipcode.classification_code': str,
            'zipcode.city_alias_code': str, 'zipcode.facility_code':str}
zip_data=pd.read_csv(r'zip_code.csv',dtype=dtype_dic)
zip_data

zip_data.columns

zip_x=['zipcode.zip', 'zipcode.fsa','zipcode.population', 'zipcode.households_per_zipcode', 
       'zipcode.white_population', 'zipcode.black_population', 'zipcode.hispanic.population', 'zipcode.asian_population',
       'zipcode.hawaiian_population', 'zipcode.indian_population', 'zipcode.other_population', 
       'zipcode.male_population', 'zipcode.female_population', 
       'zipcode.persons_per_household', 'zipcode.avarage_house_value', 'zipcode.income_per_household', 
       'zipcode.latitude', 'zipcode.longitude', 'zipcode.elevation', 'zipcode.state_full_name', 'zipcode.city_type',
       'zipcode.city', 'zipcode.country', 'zipcode.county', 'zipcode.region', 'zipcode.division',
       'zipcode.mailing_name', 'zipcode.preferred_last_line_key', 'zipcode.classification_code', 'zipcode.multi_county',
       'zipcode.csa_name', 'zipcode.cbsa_div_name', 'zipcode.city_state_key', 'zipcode.city_alias_code',
       'zipcode.city_mixed_case', 'zipcode.city_alias_mixed_case', 'zipcode.state_ansi', 'zipcode.county_ansi', 'zipcode.facility_code',
       'zipcode.city_delivery_indicator', 'zipcode.carrier_route_rate_sortation', 'zipcode.finance_number']
#delete zipcode.primary_record, since 902725 rows are labled as P, the rest are missing.-useless
#delete zipcode.city_alias_mixed_case,zipcode.unique_zip_name
#delete some columns that are some detailed info about zipcode itself or are redundent, such as zipcode.city_alias_abbreviation,
#zipcode.area_code,zipcode.city_alias_name,zipcode.county_fips(sequent number),zipcode.state_fips, zipcode.state_fips,zipcode.time_zone ect.


#delete rows with same zip for further join
zip_data1=zip_data.drop_duplicates('zipcode.zip')[zip_x]
zip_data1

missing_rate(zip_data1,'zip_data1')

#delete columns that have a missing rate>95%
zip_x1=['zipcode.zip' ,'zipcode.population', 'zipcode.households_per_zipcode', 
       'zipcode.white_population', 'zipcode.black_population', 'zipcode.hispanic.population', 'zipcode.asian_population',
       'zipcode.hawaiian_population', 'zipcode.indian_population', 'zipcode.other_population', 
       'zipcode.male_population', 'zipcode.female_population', 
       'zipcode.persons_per_household', 'zipcode.avarage_house_value', 'zipcode.income_per_household', 
       'zipcode.latitude', 'zipcode.longitude', 'zipcode.elevation', 'zipcode.state_full_name', 'zipcode.city', 'zipcode.country']

zip_data2=zip_data1[zip_x1]
zip_data2

#left join lead data and zip data
data=pd.merge(lead_data1,zip_data2,how='left',left_on='zip',right_on='zipcode.zip')
del data['zipcode.zip']   
data

US_data=data[data['zipcode.country']=='US']
missing_rate(US_data,'US data')

#create two name column to store year and month, recode CN's subordinates to CN
US_data['received_year']=US_data['received_time'].apply(lambda x:x[:4])
US_data['received_month']=US_data['received_time'].apply(lambda x:x[5:7])
CN=['CN - Fence Nation','CN - General','CN - HVAC Nation','CN - Remodeling Nation','CN - Restoration Nation','CN - Roofing Nation','CN Go!']
def association_recode(x):
    if x in CN:
        return 'CN'
    else:
        return x
US_data['association']=US_data['association'].apply(lambda x:association_recode(x))

#delete rows where missing rate <1%, dropped 6991 rows in total
US_data1=US_data.dropna(subset = ['association','source','service_type','company','zipcode.state_full_name'])
missing_rate(US_data1,'US_data1')

US_data1.rename(columns={'zipcode.population':'population','zipcode.households_per_zipcode':'households_per_zipcode',
                        'zipcode.white_population':'white_population','zipcode.black_population':'black_population',
                        'zipcode.hispanic.population':'hispanic.population','zipcode.asian_population':'asian_population',
                        'zipcode.hawaiian_population':'hawaiian_population','zipcode.indian_population':'indian_population',
                        'zipcode.other_population':'other_population','zipcode.male_population':'male_population',
                        'zipcode.female_population':'female_population', 'zipcode.persons_per_household':'persons_per_household',
                        'zipcode.avarage_house_value':'avarage_house_value','zipcode.income_per_household':'income_per_household',
                        'zipcode.latitude':'latitude','zipcode.longitude':'longitude', 'zipcode.elevation':'elevation',
                        'zipcode.state_full_name':'state_full_name','zipcode.city':'city', 'zipcode.country':'country'},inplace=True)
US_data1.to_csv('US_data1.csv',index=False)


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
divisions = ['Northeast']*11 + ['Central']*7 + ['East North Central']*4 + ['Northwest']*3 + ['South']*6 + ['Southeast']*6 + ['Southwest']*4 + ['West']*2 + ['West North Central']*5 + ['Other']*3
        
#Create Dataframe which column is regional division and index is states' name
state_division = pd.DataFrame({'division': divisions}, index=state_names)

#Join DF'state_division' to US_data
US_data1 = pd.merge(US_data1, state_division, left_on='state_full_name', right_index=True)

US_data1 = US_data1.drop('country', axis=1)

US_data1.to_csv('US_data1.csv',index=False)

#
ud = pd.read_csv('US_data1.csv')
ud.avarage_house_value.mean()

