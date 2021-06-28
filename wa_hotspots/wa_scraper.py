import pandas as pd 
import os 
from bs4 import BeautifulSoup as bs
from modules.yachtCharter import yachtCharter


print("Grabbing WA hotspot chart")

here = os.path.dirname(__file__)
data_path = os.path.dirname(__file__) + "/data/"
output_path = os.path.dirname(__file__) + "/output/"

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

urlo = 'https://healthywa.wa.gov.au/Articles/A_E/Coronavirus/Locations-visited-by-confirmed-cases'

options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)
driver.get(urlo)

html = driver.page_source

## GRAB THE HEADLINES FROM THE COLLAPSABLE BUTTONS
soup = bs(html, 'html.parser')
callums = soup.find_all(class_="doh-accordian_btn")
callums = [x.text for x in callums]
callums = [x.replace("Public exposure sites – ", '') for x in callums]
callums = [x.strip() for x in callums]

callums = [x for x in callums if x.lower() != "flights"]

tables = pd.read_html(html)

listo = []

for i in range(0,len(callums)):
    table = tables[i]

    if table.columns[0] == 0:
        table.columns = table.iloc[0]
        table = table[1:]
        table['Health advice'] = callums[i]

    listo.append(table)

final = pd.concat(listo)

final['Date'] = pd.to_datetime(final['Date'])
final['Date'] = final['Date'].dt.strftime('%d/%m/%Y')

# print(final)

print("Making WA hotspot chart")

def makeTable(df):
	
    template = [
            {
                "title": "Western Australia Covid Hotspots",
                "subtitle": f"""""",
                "footnote": "",
                "source": "Western Australia government",
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
    options=[{"colorScheme":"guardian","format": "scrolling","enableSearch": "TRUE","enableSort": "TRUE"}], chartName="wa_covid_hotspots")

makeTable(final)