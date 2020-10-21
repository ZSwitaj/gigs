# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 16:27:18 2020

@author: Administrator
"""

import matplotlib.pyplot as plt
import pandas as pd
from pytrends.request import TrendReq
from datetime import date

def getTrendData(keyword):

    dataset= []
    
    end_date = date(2020,9,26)
    start_date = date(2019, 9, 1)
    timeFrame = start_date.strftime('%Y-%m-%d')+' ' + end_date.strftime("%Y-%m-%d")
    
    pytrends = TrendReq(hl='en-US', tz=360)
    
    pytrends.build_payload(kw_list = [keyword],
                            timeframe = timeFrame,
                            geo = 'US')
    data = pytrends.interest_over_time()
    if not data.empty:
        data = data.drop(labels = ['isPartial'], axis ='columns')
        dataset.append(data)
            
    dataset = pd.concat(dataset, axis = 1)
    
    lastYear = dataset.head(4)
    thisYear = dataset.tail(4)
    
    plt.plot(range(4),lastYear, color='blue', label = 'Last Year')
    plt.plot(range(4), thisYear, color= 'orange', label = 'This Year')
    plt.legend()
    
    df = pd.DataFrame()
    df = df.append(lastYear)
    df = df.append(thisYear)
    
    yoyIncrease = ((thisYear.mean(axis=0)[0] - lastYear.mean(axis=0)[0]) / lastYear.mean(axis=0)[0]) * 100
    
    # print(pytrends.suggestions(keyword))
    
    print("\n" + keyword + ": " + str(round(yoyIncrease,2)))
          
kw_list = ("Timberland Boots", "UGG", "Dr. Martens", "Merrell", "The North Face",
           "Patagonia", "ALlbirds", "Vans", "Jimmy Choo")


for i in range(len(kw_list)):
    getTrendData(kw_list[i])