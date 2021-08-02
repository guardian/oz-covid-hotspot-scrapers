#%%
# from modules.yachtCharter import yachtCharter
import pandas as pd

import datetime
import pytz

today = datetime.datetime.now(pytz.timezone("Australia/Sydney"))
today = datetime.datetime.strftime(today, '%d/%m/%Y')

nsw = 'https://raw.githubusercontent.com/joshnicholas/exposure_site_scrapers/main/data/nsw_exposure_sites.csv'
vic = 'https://raw.githubusercontent.com/joshnicholas/exposure_site_scrapers/main/data/vic_exposure_sites.csv'
qld = 'https://raw.githubusercontent.com/joshnicholas/exposure_site_scrapers/main/data/qld_exposure_sites.csv'
wa = 'https://raw.githubusercontent.com/joshnicholas/exposure_site_scrapers/main/data/wa_exposure_sites.csv'

#%%

nsw = pd.read_csv(nsw)
vic = pd.read_csv(vic, error_bad_lines=False)
# vic = vic.loc[vic['Exposure day'] != "Anyone who has visited this location during these times should urgently get tested, then isolate until confirmation of a negative result. Continue to monitor for symptoms, get tested again if symptoms appear."]
# vic = vic.loc[vic['Exposure day'] != "9:00pm - 10:30pm"]
# vic['Exposure day'] = pd.to_datetime(vic['Exposure day']).dt.strftime('%Y-%m-%d')



qld = pd.read_csv(qld)
wa = pd.read_csv(wa)

# nsw = nsw.drop_duplicates(subset=['Venue', 'Date'])
# qld = qld.drop_duplicates(subset=['Date', 'Place'])

# vic = vic.drop_duplicates(subset=['Site', 'Exposure day'])
# wa = wa.drop_duplicates(subset=['Address', 'Date'])

nsw = nsw[['Date', 'Suburb']]
vic = vic[['Exposure day', 'Suburb']]
qld = qld[['Date', 'Suburb']]
wa = wa[['Date', 'Location']]

wa.columns = ['Date', 'Suburb']
vic.columns = ['Date', 'Suburb']

nsw['State'] = "NSW"
vic['State'] = "VIC"
qld['State'] = "QLD"
wa['State'] = "WA"

print(nsw)
print(vic)
print(qld)
print(wa)

combo = nsw.append(vic)
combo = combo.append(qld)
combo = combo.append(wa)

with open("exposure_count.csv", "w") as f:
    combo.to_csv(f, index=False, header=True)


#%%

## GRAB QUEENSLAND

# nsw = nsw[['Date', 'Suburb']]
# vic = vic[['Exposure day', 'Suburb']]
# qld = qld[['Date', 'Suburb']]
# wa = wa[['Date', 'Location']]

# wa.columns = ['Date', 'Suburb']
# vic.columns = ['Date', 'Suburb']

# vic = vic.dropna(subset=["Date"])

# vic_1 = vic.loc[~vic['Date'].str.contains("2021")]

# vic_1['Date'] = pd.to_datetime(vic_1['Date']).dt.strftime('%Y-%m-%d')

# vic_1['Date'] = vic_1['Date'].str.split("/")

# vic_2 = vic.loc[vic['Date'].str.contains("2021")]

# print(vic_1)
# print(vic_2)

# # vic['Date'] = pd.to_datetime(vic['Date']).dt.strftime('%Y-%m-%d')

# # vic['Date'] = vic['Date'].map(lambda x: pd.to_datetime(x.strip(), format="d/%m/%Y") if "2021" in x else pd.to_datetime(x, format="%d/%m/%y"))
# # vic['Date'] = vic['Date'].map(lambda x: pd.to_datetime(x) if "2021" in x else pd.to_datetime(x))

# # vic['Date'] = pd.to_datetime(vic['Date'])

# # vic['Date'] = vic['Date'].map(lambda x: x.split("/"))

# # print(vic['Date'].unique().tolist())

# # vic = vic[:-96]

# # vic['Date'] = pd.to_datetime(vic['Date'])
# vic['Date'] = pd.to_datetime(vic['Date'], format="%d/%m/%Y").dt.strftime('%Y-%m-%d')
# qld['Date'] = pd.to_datetime(qld['Date'], format="%A %d %B %Y").dt.strftime('%Y-%m-%d')
# wa['Date'] = pd.to_datetime(wa['Date'], format="%d/%m/%Y").dt.strftime('%Y-%m-%d')

# vic['Date'] = pd.to_datetime(vic['Date']).dt.strftime('%Y-%m-%d')
# qld['Date'] = pd.to_datetime(qld['Date']).dt.strftime('%Y-%m-%d')
# wa['Date'] = pd.to_datetime(wa['Date']).dt.strftime('%Y-%m-%d')


# print(vic)


# nsw.loc[nsw['Date'] == 'Friday 25 June 2021 to Saturday 26 June 2021', 'Date'] = "Friday 25 June 2021"
# nsw.loc[nsw['Date'] == 'Tuesday 22 June 2021 - Wednesday 23 June 2021', 'Date'] = "Tuesday 22 June 2021"

# nsw['Date'] = nsw['Date'].str.replace("  ", " ")

# nsw['Date'] = nsw['Date'].str.replace(",", "")

# nsw['Date'] = nsw['Date'].str.replace("1932", "2021")

# # nsw['Date'] = nsw['Date'].apply(lambda x: x.strip() + " 2021" if "2021" not in x else x.strip())

# # nsw['Date'] = nsw['Date'].str.replace("  ", " ")

# # nsw['Date'] = pd.to_datetime(nsw['Date'], format="%A %d %B %Y").dt.strftime('%Y-%m-%d')


# nsw['Date'] = nsw['Date'].map(lambda x: pd.to_datetime(x.strip(), format="%A %d %B %Y") if "2021" in x else pd.to_datetime(x.strip(), format="%A %d %B"))

# # nsw['Date'] = nsw['Date'].dt.year 

# nsw['Date'] = nsw['Date'].dt.strftime('%Y-%m-%d')

# nsw['Date'] = nsw['Date'].str.replace("1900", "2021")

# # print(vic['Date'].unique().tolist())


# # nsw['Date'] = nsw['Date'].apply(lambda x: x.strip() + " 2021" if "2021" not in x else x.strip())

# # nsw['Date'] = pd.to_datetime(nsw['Date'])

# # # nsw['Date'] = pd.to_datetime(nsw['Date'], format="%A %d %B %Y")
# # # print(nsw['Date'].unique().tolist())

# # wa.columns = ['Date', 'Suburb']

# nsw['State'] = "NSW"
# vic['State'] = 'VIC'
# qld['State'] = 'QLD'
# wa['State'] = 'WA'

# combo = pd.concat([nsw, vic, qld, wa])



# # print(combo['Date'].unique().tolist())
# # %%

# # combo['Date'] = combo['Date'].str.split(" to ")[0]


# # combo['Date'] = pd.to_datetime(combo['Date'])
# combo['Count'] = 1



# combo = combo.groupby(by=["Date", "State"])['Count'].sum().reset_index()

# # print(combo.loc[combo['State'] == "QLD"])

# # combo['Date'] = combo['Date'].dt.strftime('%Y-%m-%d')

# combo = combo.pivot(index="Date", columns="State")['Count'].reset_index()

# # combo.columns.name=None
# # combo.index.name = None

# # combo.set_index('Date', inplace=True)

# # print(combo)
# # print(combo.columns)
# # %%

# # print(nsw['Date'].unique().tolist())
# # %%

# # print(combo)
# # # print(combo.columns)

# # def makestackedbar(df):

# #     template = [
# #             {
# #                 "title": "Exposure sites by state",
# #                 "subtitle": f"""Showing the number of exposure sites by day of exposure. Last updated {today}""",
# #                 "footnote": "",
# #                 "source": "| Sources: State government websites",
# #                 "dateFormat": "%Y-%m-%d",
# #                 "minY": "0",
# #                 "maxY": "",
# #                 "xAxisDateFormat":"%b %d",
# #                 "tooltip":"<strong>{{#formatDate}}{{data.Date}}{{/formatDate}}</strong><br/>{{group}}: {{groupValue}}<br/>Total: {{total}}",
# #                 "margin-left": "50",
# #                 "margin-top": "30",
# #                 "margin-bottom": "20",
# #                 "margin-right": "10"
# #             }
# #         ]
# #     key = []
# #     periods = []
# #     # labels = []
# #     df.fillna("", inplace=True)
# #     chartData = df.to_dict('records')
# #     labels = []


# #     yachtCharter(template=template, labels=labels, data=chartData, chartId=[{"type":"stackedbar"}], chartName="oz-exposure-sites")

# # # makestackedbar(combo)
