#%%
from numpy import column_stack
import pandas as pd
import requests
from modules.yachtCharter import yachtCharter
import os
import re

print("Grabbing ACT hotspot data")

# testo = "_test"
testo = ''

chart_key = "act_covid_hotspots"

#%%

data_path = os.path.dirname(__file__)
pd.set_option("display.max_rows", None, "display.max_columns", None)

headers = {'user-agent': 'The Guardian'}
html = requests.get('https://www.covid19.act.gov.au/act-status-and-response/act-covid-19-exposure-locations', headers=headers).text
tables = pd.read_html(html)

table_labels = ['Close contact', 'Casual contact exposure', 'Monitor for symptoms']

cols = ["Suburb","Place","Date","Arrival Time","Departure Time"]

listo = []

for i in range(0, len(table_labels)):
    inter = tables[i].copy()
    inter.columns = [x.title() for x in inter.columns]
    # print(inter)
    # print(inter.columns)
    inter = inter[cols]
    inter['Type'] = table_labels[i]
    listo.append(inter)


df = pd.concat(listo)

## ATTEMPT TO SORT BY LATEST:
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