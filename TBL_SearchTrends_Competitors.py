import pandas as pd
import time
from pytrends.request import TrendReq
startTime = time.time()

pytrends = TrendReq(hl = 'en-US', tz = 360)

colnames = ["keywords"]
df = pd.read_csv("keywords_brands.csv", names = colnames)
df2 = df["keywords"].values.tolist()
df2.remove("Keywords")

dataset = [] #data set for this years data
datasetLY = [] # data set for last years data

for x in range(0, len(df2)):
    keywords = [df2[x]]
    pytrends.build_payload(kw_list = keywords,
                            cat = 0,
                            timeframe = '2020-09-01 2020-09-30',
                            geo = 'US')
    data = pytrends.interest_over_time()
    if not data.empty:
        data = data.drop(labels = ['isPartial'], axis ='columns')
        dataset.append(data)
        
dataset = pd.concat(dataset, axis = 1)

with open('brands_trends.csv', 'w+') as file:
    dataset.to_csv(file, header = True)
file.close()

executionTime = (time.time() - startTime)
print('Execution time: ' + str(executionTime) + ' sec')


