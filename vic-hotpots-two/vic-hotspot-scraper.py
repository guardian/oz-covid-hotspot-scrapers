import requests
import pandas as pd 
import os 
from modules.yachtCharter import yachtCharter

here = os.path.dirname(__file__)
file_name = 'vic-hotspot_download.csv'

ceevee = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSNouXrJ8UQ-tn6bAxzrOdLINuoOtn01fSjooql0O3XQlj4_ldFiglzOmDm--t2jy1k-ABK6LMzPScs/pub?gid=1075463302&single=true&output=csv'

# r = requests.get(ceevee)

# with open(f"{here}/{file_name}", 'wb') as f:
#     f.write(r.content)

print("hi")

df = pd.read_csv(f"{here}/{file_name}")

df['Added_date_dtm'] = pd.to_datetime(df['Added_date_dtm'])

df = df.sort_values(by='Added_date_dtm', ascending=False)

df = df[['Suburb', 'Site_title','Exposure_date', 'Exposure_time',
       'Notes', 'Added_date', 'Advice_instruction' ]]



df.columns = ['Suburb', 'Site', 'Exposure day', 'Exposure time', 'Notes', 'Date added', 'Health advice']

def makeTable(df):
	
    template = [
            {
                "title": "Victoria Covid Hotspots",
                "subtitle": f"""""",
                "footnote": "",
                "source": "| Sources: Victorian government",
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
    options=[{"colorScheme":"guardian","format": "scrolling","enableSearch": "TRUE","enableSort": "TRUE"}], chartName="vic_covid_hotspots")

makeTable(df)