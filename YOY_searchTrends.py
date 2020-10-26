import pandas as pd
from pytrends.request import TrendReq
from datetime import date

def getTrendData(keyword):

    dataset= []
    
    end_date = date(2020,8,29)
    start_date = date(2019, 7, 28)
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

    # print("\n" + keyword + ": " + str(round(yoyIncrease,1)))

    return yoyIncrease

def getSuggestions(keyword):
    
    pytrends = TrendReq(hl='en-US', tz=360)
    
    suggestions = (pytrends.suggestions(keyword))
    suggestions = pd.DataFrame(suggestions)
    
    return suggestions
          
# kw_list = ("Zappos", "Foot Locker", "Genesco", "Designer Brands", "Nordstrom", 
#             "Macy's", "REI", "Dicks", 
#             "Boot", "Outerwear")

# kw_list = ("Timberland", "Timberland Boots", "UGG", "Dr. Martens", "Merrell", 
#             "The North Face", "Patagonia", "Allbirds", "Vans", "Amazon", 
#             "Walmart", "Target")

# kw_list = ("/m/05kv16","/m/06wccjq")

kw_dict = {
    "Timberland": "",
    "UGG": "/m/06wccjq",
    "Dr Martens": "/m/01lsm6",
    "Merrell": "/m/0kqrz3",
    "The North Face": "/m/04n92b",
    "Patagonia": "/m/0g152j",
    "Allbirds": "/g/11g6j4k3hl",
    "Vans": "/m/04kbwy",
    "Amazon": "/m/0mgkg ",
    "Walmart": "/m/0841v",
    "Target": "/m/072p41",
    }

kw_list = ("Target",)

# for i in range(len(kw_list)):
#     getTrendData(kw_list[i])

# for topic in kw_dict:
#     print("{}: {}".format(topic, getTrendData(kw_dict[topic])))

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    