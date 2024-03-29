import pandas as pd
import time
from pytrends.request import TrendReq
import streamlit as st
startTime = time.time()

pytrends = TrendReq(hl = 'en-US', tz = 360)

colnames = ["keywords"]
df = pd.read_csv("keyword_list.csv", names = colnames)
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
    data = pytrends.interest_by_region(resolution='COUNTRY', inc_low_vol = False, inc_geo_code = False)
    if not data.empty:
        # data = data.drop(labels = ['isPartial'], axis ='columns')
        dataset.append(data)

for x in range(0, len(df2)):
    keywords = [df2[x]]
    pytrends.build_payload(kw_list = keywords,
                            cat = 0,
                            timeframe = '2019-09-01 2019-09-30',
                            geo = 'US')
    data = pytrends.interest_by_region(resolution='COUNTRY', inc_low_vol = False, inc_geo_code = False)
    if not data.empty:
        # data = data.drop(labels = ['isPartial'], axis ='columns')
        datasetLY.append(data)
        
dataset = pd.concat(dataset, axis = 1)
datasetLY = pd.concat(datasetLY, axis = 1)

dataset = dataset.rename(columns = {'Timberland Boots': 'TBL'})
datasetLY = datasetLY.rename(columns = {'Timberland Boots': 'TBL -1y'})

df = dataset.merge(datasetLY, how = 'outer', left_index = True, right_index = True)

df['YOY change'] = round((df['TBL']-df['TBL -1y'])/df['TBL -1y'] * 100,1)
df['Abs Change'] = abs(df['YOY change'])
df = df.sort_values(by= ['Abs Change'], ascending = False)
df = df.drop(columns = ['Abs Change'])
# df = df.transpose()

# with open('search_trends_byStateYOY.csv', 'w+') as file:
#     df.to_csv(file, header = True)
# file.close()

executionTime = (time.time() - startTime)
print('Execution time: ' + str(executionTime) + ' sec')

"""
Streamlit Code
"""

st.title('Google Trends Data for Timberland')

st.subheader('Raw data')
st.write(df)

st.line_chart(df)







































