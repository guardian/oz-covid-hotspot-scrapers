import requests
import pandas as pd 
from bs4 import BeautifulSoup as bs 
from modules.yachtCharter import yachtCharter
import re

print("Grabbing ACT hotspot data")

# testo = "_test"
testo = ''

chart_key = "act_covid_hotspots"


headers = {'user-agent': 'The Guardian'}
html = requests.get('https://www.covid19.act.gov.au/act-status-and-response/act-covid-19-exposure-locations', headers=headers).text
# tables = pd.read_html(html)

soup = bs(html, 'html.parser')
finder = soup.find_all('script', type='text/javascript')

ceevee = re.search("(?P<url>https?://[^\s]+)", finder[0].string).group("url")
ceevee = ceevee.replace('",', "").strip()

df = pd.read_csv(ceevee)

df = df.iloc[: , 2:]

df = df[df.columns[range(8)]]

df.columns = ['Location', 'Address', 'Suburb', 'State', 'Date', 'Arrival Time', 'Departure Time', 'Contact']

df = df[['Suburb', 'Location' , 'Address', 'Date', 'Arrival Time', 'Departure Time', 'Contact']]

## ATTEMPT TO SORT BY LATEST:
try:
    # df['Date_2'] = df['Date'].apply(lambda x: x.strip() + " 2021" if "2021" not in x else x.strip())
    df['Sort'] = pd.to_datetime(df['Date'], format="%d/%m/%Y - %A")
    df = df.sort_values(by=['Sort'], ascending=False)
    # print(df['Sort'])
    df.drop(columns=['Sort'], inplace=True)
except Exception as e:
    print(e)
    pass

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