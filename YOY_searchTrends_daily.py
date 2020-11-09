import pandas as pd
from pytrends.request import TrendReq
from datetime import timedelta, date

"""
One year from today
"""

# keyword = "/m/04n92b"

overlap_days = 30
overlap_time = timedelta(days = overlap_days)

this_start_date = date(2020,3,24)- overlap_time
this_end_date = date(2020,10,24)
last_start_date = date(2019,9,29)
last_end_date = this_start_date + overlap_time - timedelta(days = 1)
    
def getTrendData(keyword, start_date, end_date):
    
    pytrends = TrendReq(hl='en-US', tz=360)
    dataset = []

    timeFrame = start_date.strftime('%Y-%m-%d')+' ' + end_date.strftime("%Y-%m-%d")
    
    pytrends.build_payload(kw_list = [keyword],
                        timeframe = timeFrame,
                        geo = 'US')
    data = pytrends.interest_over_time()
    if not data.empty:
        data = data.drop(labels = ['isPartial'], axis ='columns')
        dataset.append(data)
            
    dataset = pd.concat(dataset, axis = 1)
    
    return dataset

def getCorrFactors(lastYearData, thisYearData):

    correctionFactors = []
    i = 0
    lastYearTail = pd.DataFrame(lastYearData.tail(overlap_days))
    thisYearHead = pd.DataFrame(thisYearData.head(overlap_days))
    for i in range(len(lastYearTail)):
        correctionFactors.append((lastYearTail.iloc[i][0]/thisYearHead.iloc[i][0]))
        i += 1
        
    return sum(correctionFactors)/len(correctionFactors)

def correctDailyData(data, correctionFactor):
    return data / correctionFactor

def calcYOY(keyword, this_start_date = this_start_date, this_end_date = this_end_date,
            last_start_date = last_start_date, last_end_date = last_end_date):
    
    thisYear = getTrendData(keyword, this_start_date, this_end_date)
    lastYear = getTrendData(keyword, last_start_date, last_end_date)
    corr = getCorrFactors(lastYear, thisYear)
    corrLastYear = correctDailyData(lastYear, corr)
    
    thisYearAns = thisYear.tail(28).mean(axis=0)[0]
    lastYearAns = corrLastYear.head(28).mean(axis=0)[0]
    
    yoyIncrease = ((thisYearAns - lastYearAns)/ lastYearAns) * 100
    
    return str(round(yoyIncrease, 1)) + "%"
    
kw_dict = {
    "Timberland": "/m/05kv16",
    "Timberland Boots": "Timberland Boots",
    "UGG": "/m/06wccjq",
    "Dr Martens": "/m/01lsm6",
    "Merrell": "/m/0kqrz3",
    "The North Face": "/m/04n92b",
    "Patagonia": "/m/0g152j",
    "Allbirds": "/g/11g6j4k3hl",
    "Vans": "/m/04kbwy",
    "Amazon": "/m/0mgkg ",
    "Walmart": "/m/0841v",
    "Target": "/m/01b39j",
    "Zappos": "/m/02dfb9",
    "Foot Locker": "/m/08fhy9",
    "Journeys": "/m/03cbgd",
    "DSW": "/m/0flp70",
    "Nordstrom": "/m/01fc_q",
    "Macy's": "/m/01pkxd ",
    "REI": "/m/02nx4d",
    "Dick's Sports": "/m/06fgv_",
    "Boot": "/m/01b638",
    "Outerwear": "/m/047vlmn"
    }

lst_keywords = []

print("Adding keywords...")
for topic in kw_dict:
    lst_keywords.append(topic)


lst_values = []

print("Calculating...")
for topic in kw_dict:
    print(topic)
    lst_values.append(calcYOY(kw_dict[topic]))

print("Combining...")
res = dict(zip(lst_keywords, lst_values))
res_df = pd.DataFrame.from_dict(res, orient = 'index', columns = ['YOY Change'])
res_df = res_df.transpose()

# thisYear = getTrendData(keyword, this_start_date, this_end_date)
# lastYear = getTrendData(keyword, last_start_date, last_end_date)
# corr = getCorrFactors(lastYear, thisYear)
# corrLastYear = correctDailyData(lastYear, corr)

# import matplotlib.pyplot as plt

# plt.scatter(thisYear.head(30), corrLastYear.tail(30))
