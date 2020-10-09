# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 12:56:57 2020

@author: Administrator
"""

import pandas as pd
import pytrends
from pytrends.request import TrendReq
pytrend = TrendReq()

KEYWORDS = ['Nike', 'The North Face', 'Vans', 'The Timberland Company']
KEYWORDS_CODES = [pytrend.suggestions(keyword = i)[0] for i in KEYWORDS]
df_CODES = pd.DataFrame(KEYWORDS_CODES)

EXACT_KEYWORDS = df_CODES['mid'].to_list()
DATE_INTERVAL = '2020-09-01 2020-9-30'
COUNTRY = ['US','GB','DE']
CATEGORY = 0
SEARCH_TYPE = ''

Individual_EXACT_KEYWORD = list(zip(*[iter(EXACT_KEYWORDS)]*1))
Individual_EXACT_KEYWORD = [list(x) for x in Individual_EXACT_KEYWORD]
dicti = {}
i = 1
for Country in COUNTRY:
    for keyword in Individual_EXACT_KEYWORD:
            pytrend.build_payload(kw_list=keyword,
                                  timeframe = DATE_INTERVAL,
                                  geo = Country,
                                  cat=CATEGORY,
                                  gprop=SEARCH_TYPE)
            dicti[i] = pytrend.interest_over_time()
            i+=1
df_trends = pd.concat(dicti, axis=1)

df_trends.columns = df_trends.columns.droplevel(0) #drop outside header
df_trends = df_trends.drop('isPartial', axis = 1) #drop "isPartial"
df_trends.reset_index(level=0,inplace=True) #reset_index

df_trends.columns=['date','Nike-US','The North Face-US','Vans-US',
                   'The Timberland Company-US','Nike-UK','The North Face-UK',
                   'Vans-UK', 'The Timberland Company-UK','Nike-Germany',
                   'The North Face-Germany','Vans-Germany',
                   'The Timberland Company-Germany']

import seaborn as sns
sns.set(color_codes=True)
dx = df_trends.plot(figsize = (12,8), x = 'date', 
                    y = ['The Timberland Company-US','Vans-US',
                         'The North Face-US'], 
                    kind = 'line', title = 'VF Brands Google Trends')
dx.set_xlabel('Date')
dx.set_ylabel('Trends Index')
dx.tick_params(axis = 'both', which = 'both', labelsize = 10)
