import pandas as pd
from pytrends.request import TrendReq
from datetime import date

def getTrendData(keyword):

    dataset= []
    
    end_date = date(2020,10,24)
    start_date = date(2019, 9, 29)
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
    
    df = pd.DataFrame()
    df = df.append(lastYear)
    df = df.append(thisYear)

    yoyIncrease = ((thisYear.mean(axis=0)[0] - lastYear.mean(axis=0)[0]) / lastYear.mean(axis=0)[0]) * 100

    return yoyIncrease

def getSuggestions(keyword):
    
    pytrends = TrendReq(hl='en-US', tz=360)
    
    suggestions = (pytrends.suggestions(keyword))
    suggestions = pd.DataFrame(suggestions)
    
    return suggestions

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
    lst_values.append(round(getTrendData(kw_dict[topic]),1))

print("Combining...")
res = dict(zip(lst_keywords, lst_values))
res_df = pd.DataFrame.from_dict(res, orient = 'index', columns = ['YOY Change'])
res_df = res_df.transpose()

res_df.to_csv(r'output.csv')

    
    
    