import pandas as pd
from pytrends.request import TrendReq
from datetime import timedelta, datetime, date

"""
One year from today
"""

YEAR = 2020
MONTH = 9

def getTrendData(keyword, year = YEAR, month = MONTH):
    
    pytrends = TrendReq(hl='en-US', tz=360)
    dataset = []
    # end_date = datetime.now()
    end_date = date(year ,month, getLastDayOfMonth(year,month))
    start_date = date(year-1, month, 1)
    thisYear = start_date.strftime('%Y-%m-%d')+' ' + end_date.strftime("%Y-%m-%d")
    
    pytrends.build_payload(kw_list = [keyword],
                        timeframe = thisYear)
    data = pytrends.interest_over_time()
    if not data.empty:
        data = data.drop(labels = ['isPartial'], axis ='columns')
        dataset.append(data)
            
    dataset = pd.concat(dataset, axis = 1)
    
    return dataset

def getYOYCorrFactors(trendData):
    
    correctionFactors = []
    i = 0
    lastYear = pd.DataFrame(trendData.head(4))
    thisYear = pd.DataFrame(trendData.tail(4))
    for i in range(len(lastYear)):
        correctionFactors.append((lastYear.iloc[i][0])/thisYear.iloc[i][0])
        i += 1

    return sum(correctionFactors)/len(correctionFactors)

def getYOYCorrFactors2(trendData):

    lastYear = pd.DataFrame(trendData.head(4)).mean(axis=0)[0]
    thisYear = pd.DataFrame(trendData.tail(4)).mean(axis=0)[0]
    
    return lastYear/thisYear
    
def getLastDayOfMonth(year, month):
    leapYear = False
    if (year % 4) == 0:
       if (year % 100) == 0:
           if (year % 400) == 0:
               leapYear = True
       else:
           leapYear = True

    thirtyDays = (4,6,9,11)
    
    if month == 2:
        if leapYear:
            return 29
        else:
            return 28
    elif month in thirtyDays:
        return 30
    else:
        return 31

def getDailyData(keyword, year = YEAR, month = MONTH):
    
    monthData = []
    end_date = date(year, month, getLastDayOfMonth(year, month))
    start_date = date(year, month, 1)
    DATE_INTERVAL = start_date.strftime('%Y-%m-%d')+' ' + end_date.strftime("%Y-%m-%d")
    
    pytrends = TrendReq(hl='en-US', tz=360)

    pytrends.build_payload(kw_list= [keyword],
                           timeframe = DATE_INTERVAL,
                           geo = 'US')
    data = pytrends.interest_over_time()
    if not data.empty:
        data = data.drop(labels = ['isPartial'], axis ='columns')
        monthData.append(data)
        
    monthData = pd.concat(monthData, axis = 1)
        
    return monthData

def correctDailyData(data, correctionFactor):
    return data * correctionFactor


keyword = "Timberland Boots"

# pytrends = TrendReq(hl='en-US', tz=360)
# df = pytrends.get_historical_interest([keyword], year_start=2020, month_start=9, day_start=1, hour_start=0, year_end=2020, month_end=10, day_end=1, hour_end=0, cat=0, geo='', gprop='', sleep=0)
# 
# corrFactor = (getYOYCorrFactors(getTrendData(keyword)) + getYOYCorrFactors2(getTrendData(keyword))) / 2
# thisYear = getDailyData(keyword).mean(axis=0)[0]
# lastYear = correctDailyData(getDailyData(keyword, year = 2019, month = 9),corrFactor).mean(axis=0)[0]

# yoyIncrease = ((thisYear - lastYear) / lastYear) * 100

# print(keyword + ": " + str(yoyIncrease) + "%")


""" 
Graph This Year vs Last
"""

# import matplotlib.pyplot as plt

# dataset= []

# end_date = datetime.now()
# start_date = end_date - timedelta(days = 365 * 2)
# thisYear = start_date.strftime('%Y-%m-%d')+' ' + end_date.strftime("%Y-%m-%d")

# pytrends = TrendReq(hl='en-US', tz=360)

# pytrends.build_payload(kw_list = ["Timberland Boots"],
#                         timeframe = thisYear)
# data = pytrends.interest_over_time()
# if not data.empty:
#     data = data.drop(labels = ['isPartial'], axis ='columns')
#     dataset.append(data)
        
# dataset = pd.concat(dataset, axis = 1)

# xaxis = range(1,13)

# thisYear = dataset.tail(52)
# lastYear = dataset.head(52)

# plt.plot(range(1,53), thisYear, color='blue', label = 'This Year')
# plt.plot(range(1,53), lastYear, color= 'orange', label = 'Last Year')
# plt.legend()

# twoYeardf = pd.DataFrame()
# twoYeardf = twoYeardf.append(lastYear)
# twoYeardf = twoYeardf.append(thisYear)

# twoYeardf.to_csv('two_year_data.csv')

# import matplotlib.pyplot as plt

# dataset= []

# end_date = date(2020,9,26)
# start_date = date(2019, 9, 1)
# timeFrame = start_date.strftime('%Y-%m-%d')+' ' + end_date.strftime("%Y-%m-%d")

# pytrends = TrendReq(hl='en-US', tz=360)

# pytrends.build_payload(kw_list = ["Allbirds"],
#                         timeframe = timeFrame)
# data = pytrends.interest_over_time()
# if not data.empty:
#     data = data.drop(labels = ['isPartial'], axis ='columns')
#     dataset.append(data)
        
# dataset = pd.concat(dataset, axis = 1)

# plt.plot(range(4), dataset.head(4), color='blue', label = 'Last Year')
# plt.plot(range(4), dataset.tail(4), color= 'orange', label = 'This Year')
# plt.legend()

# df = pd.DataFrame()
# df = df.append(dataset.head(4))
# df = df.append(dataset.tail(4))

# df.to_csv('testOutput.csv')





