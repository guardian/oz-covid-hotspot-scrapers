#%%
# from modules.yachtCharter import yachtCharter
import pandas as pd

import datetime
import pytz

today = datetime.datetime.now(pytz.timezone("Australia/Sydney"))
today = datetime.datetime.strftime(today, '%d/%m/%Y')

nsw = 'https://raw.githubusercontent.com/joshnicholas/exposure_site_scrapers/main/data/nsw_exposure_sites.csv'

#%%

nsw = pd.read_csv(nsw)

nsw = nsw[['Date', 'Suburb']]


#%%


nsw.loc[nsw['Date'] == 'Friday 25 June 2021 to Saturday 26 June 2021', 'Date'] = "Friday 25 June 2021"
nsw.loc[nsw['Date'] == 'Tuesday 22 June 2021 - Wednesday 23 June 2021', 'Date'] = "Tuesday 22 June 2021"

nsw['Date'] = nsw['Date'].str.replace("  ", " ")

nsw['Date'] = nsw['Date'].str.replace(",", "")

nsw['Date'] = nsw['Date'].str.replace("1932", "2021")

nsw['Date'] = nsw['Date'].apply(lambda x: x.strip() + " 2021" if "2021" not in x else x.strip())

nsw['Date'] = nsw['Date'].str.replace("  ", " ")

# nsw['Date'] = pd.to_datetime(nsw['Date'], format="%A %d %B %Y").dt.strftime('%Y-%m-%d')
nsw['Date'] = pd.to_datetime(nsw['Date'])


# %%

nsw = nsw.sort_values(by=['Date'], ascending=True)


# %%

nsw['Count'] = 1



nsw = nsw.groupby(by=["Date"])['Count'].sum().reset_index()

# print(nsw.loc[nsw['State'] == "QLD"])

# nsw['Date'] = nsw['Date'].dt.strftime('%Y-%m-%d')

# nsw = nsw.pivot(index="Date", columns="State")['Count'].reset_index()

print(nsw)

# nsw.columns.name=None
# nsw.index.name = None

# nsw.set_index('Date', inplace=True)

# print(nsw)
# print(nsw.columns)
# %%

# print(nsw['Date'].unique().tolist())
# %%

# print(nsw)
# # print(nsw.columns)

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

# # # makestackedbar(nsw)