# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 13:49:54 2020

@author: Administrator
"""

import streamlit as st
import numpy as np
import pandas as pd
import time

st.title('My first streamlit app')

st.write("Here's our first attemp at using data to create a table:")
df = pd.DataFrame({
    'first column': [1,2,3,4],
    'second column': [10,20,30,40]
 })

chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a','b','c',])

st.line_chart(chart_data)

map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50,50] + [42.975398, -70.891309],
    columns = ['lat','lon'])

st.map(map_data)

if st.checkbox('Show dataframe'):
    chart_data = pd.DataFrame(
        np.random.randn(20,3),
        columns = ['a','b','c'])
    
    st.line_chart(chart_data)
    
option = st.sidebar.selectbox(
    "Which number do you like best?",
    df['first column'])

'You selected: ', option

left_col, right_col = st.beta_columns(2)
pressed = left_col.button('Press me?')
if pressed:
    right_col.write("Woohoo!")
    
expander = st.beta_expander("FAQ")
expander.write("Here you could put in some really, really long explanations...")

'Starting a long computation...'

latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
    latest_iteration.text(f'Iteration {i+1}')
    bar.progress(i+1)
    time.sleep(0.1)
    
'... and now we are done!'