#%%
from numpy import column_stack
import pandas as pd
import requests
from modules.yachtCharter import yachtCharter
from bs4 import BeautifulSoup as bs 
import os
import re

from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium import webdriver

print("Grabbing ACT hotspot data")

# testo = "_test"
testo = ''

chart_key = "act_covid_hotspots"

#%%

options = FirefoxOptions()
options.add_argument("--headless")

browser = webdriver.Firefox(options=options)

browser.get('https://www.covid19.act.gov.au/act-status-and-response/act-covid-19-exposure-locations')

df = pd.read_html(browser.page_source)[0]

df = df[['Suburb', 'Exposure Location', 'Street', 'Date',
       'Arrival Time', 'Departure Time', 'Contact']]

df.columns = ['Suburb', 'Location', 'Street', 'Date',
       'Arrival Time', 'Departure Time', 'Contact']

try:
    df['Date_2'] = df['Date'].apply(lambda x: x.strip() + " 2021" if "2021" not in x else x.strip())
    df['Sort'] = pd.to_datetime(df['Date_2'])
    df = df.sort_values(by=['Sort'], ascending=False)
    df.drop(columns=['Sort', 'Date_2'], inplace=True)
except Exception as e:
    print(e)
    pass

# print(df.columns)
#%%
# print(df)

def makeTable(df):

    template = [
            {
                "title": "ACT Covid Hotspots",
                "subtitle": f"""""",
                "footnote": "",
                "source": "ACT Government",
                "yScaleType":"",
                "minY": "0",
                "maxY": "",
                "x_axis_cross_y":"",
                "periodDateFormat":"",
                "margin-left": "50",
                "margin-top": "30",
                "margin-bottom": "20",
                "margin-right": "10"
            }
        ]
    key = []
    # labels = []
    df.fillna("", inplace=True)
    chartData = df.to_dict('records')
    labels = []


    yachtCharter(template=template, labels=labels, data=chartData, chartId=[{"type":"table"}],
    options=[{"colorScheme":"guardian","format": "scrolling","enableSearch": "TRUE","enableSort": "TRUE"}], chartName=f"{chart_key}{testo}")

makeTable(df)