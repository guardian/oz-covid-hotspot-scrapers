import pandas as pd
import requests
from modules.yachtCharter import yachtCharter
import os
import re

print("Grabbing QLD hotspot data")

# testo = "_test"
testo = ''

data_path = os.path.dirname(__file__)
pd.set_option("display.max_rows", None, "display.max_columns", None)

headers = {'user-agent': 'The Guardian'}
html = requests.get('https://www.qld.gov.au/health/conditions/health-alerts/coronavirus-covid-19/current-status/contact-tracing', headers=headers).text
tables = pd.read_html(html)
# table_labels = ["Close contact", "Casual contact", "Historical casual contact"]

table_labels = ["Close contacts", "Casual contacts", "Low risk contacts"]

# print(tables[2])
# print(len(tables))

print("Parsing QLD hotspot data")

listo = []
for i in range(0, len(table_labels)):
    inter = tables[i]
    inter['Type'] = table_labels[i]
    listo.append(inter)


df = pd.concat(listo)


df['Place'] = df['Place'].astype(str)

## Fix issues from lack of whitespace
import re
df['Place'] = df['Place'].apply(lambda x: re.sub(r'([a-zA-Z])(\()', r'\1 \2', x))
df['Place'] = df['Place'].apply(lambda x: re.sub(r'(\))([a-zA-Z])', r'\1 \2', x))

df['Place'] = df['Place'].apply(lambda x: re.sub(r'([1-9])(\()', r'\1 \2', x))
df['Place'] = df['Place'].apply(lambda x: re.sub(r'(\))([1-9])', r'\1 \2', x))

df['Place'] = df['Place'].apply(lambda x: re.sub(r'([a-zA-Z])([1-9])', r'\1 \2', x))

# Sort descending


try:
    # df['Sort'] = pd.to_datetime(df['Date'], format="%A %d %B") + pd.offsets.DateOffset(years=121)
    df['Sort'] = pd.to_datetime(df['Date'], format="%A %d %B %Y")
    df = df.sort_values(by=["Sort", "Type"], ascending=False)
except Exception as e:
    print(e)
    pass


# print(df.columns)


df = df[['Date', 'Place', 'Suburb', 'Start of exposure', 'End of exposure','Type']]

# Drop blank row in casual contacts table
df.dropna(inplace=True)


# Parse times

# df['Arrival sort'] = df['Arrival time'].apply(lambda x: pd.to_datetime(x.replace(" ", ''), format="%I.%M%p") if "." in x else pd.to_datetime(x, format="%I%p"))
# df['Departure sort'] = df['Departure time'].apply(lambda x: pd.to_datetime(x.replace(" ", ''), format="%I.%M%p") if "." in x else pd.to_datetime(x, format="%I%p"))

# df['Arrival sort'] = df['Arrival sort'].dt.strftime("%H:%M")
# df['Departure sort'] = df['Departure sort'].dt.strftime("%H:%M")


# print(df)
# print(df.columns)
with open(f"{data_path}/hotspots.csv", "w") as f:
    df.to_csv(f, index=False, header=True)

print("Making QLD hotspot chart")

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

makeTestingLine(df)
