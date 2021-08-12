import pandas as pd
import requests
from modules.yachtCharter import yachtCharter
from bs4 import BeautifulSoup as bs 
import os
import re

print("Grabbing QLD hotspot data")

# testo = "_test"
testo = ''

data_path = os.path.dirname(__file__)
pd.set_option("display.max_rows", None, "display.max_columns", None)

headers = {'user-agent': 'The Guardian'}
r = requests.get('https://www.qld.gov.au/health/conditions/health-alerts/coronavirus-covid-19/current-status/contact-tracing', headers=headers)

soup = bs(r.text, 'html.parser')

divvy = str(soup.find(id= 'qld_combined_table_202041'))

# print(divvy)
# print(type(divvy))

table = pd.read_html(divvy)[0]

table.loc[table['Category'] == "Close", "Category"] = "Close contact"
table.loc[table['Category'] == "Casual", "Category"] = "Casual contact"
table.loc[table['Category'] == "Low risk", "Category"] = "Low risk contact"

## FIX WHITESPACE

table['Place'] = table['Place'].apply(lambda x: re.sub(r'([a-zA-Z])([1-9])', r'\1 \2', x))

try:
    # df['Sort'] = pd.to_datetime(df['Date'], format="%A %d %B") + pd.offsets.DateOffset(years=121)
    table['Sort'] = pd.to_datetime(table['Exposure date'], format="%A %d %B %Y")
    table = table.sort_values(by=["Sort", "Category"], ascending=False)
    # print(table)
except Exception as e:
    print(e)
    pass

table = table.drop(columns=['Sort'])

# print(table)


def makeTestingLine(df):

    template = [
            {
                "title": "Queensland Covid Hotspots",
                "subtitle": f"""""",
                "footnote": "",
                "source": "Queensland Department of Health",
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
    options=[{"colorScheme":"guardian","format": "scrolling","enableSearch": "TRUE","enableSort": "TRUE"}], chartName=f"qld_covid_hotspots{testo}")

makeTestingLine(table)