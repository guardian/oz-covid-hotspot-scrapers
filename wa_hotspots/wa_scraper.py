import requests 
import pandas as pd 
import os 
import time 

here = os.path.dirname(__file__)
data_path = os.path.dirname(__file__) + "/data/"
output_path = os.path.dirname(__file__) + "/output/"

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

urlo = 'https://healthywa.wa.gov.au/Articles/A_E/Coronavirus/Locations-visited-by-confirmed-cases'
# r = requests.get(urlo)

listo = []
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)
# driver = webdriver.Firefox()
driver.get(urlo)

html = driver.page_source
tables = pd.read_html(html)

callums = ['Get tested immediately and quarantine for 14 days', 'Get tested immediately, quarantine until a negative result is returned and monitor for symptoms', 'Monitor for symptoms']

listo = []

for i in range(0,len(callums)):
    table = tables[i]

    if table.columns[0] == 0:
        table.columns = table.iloc[0]
        table = table[1:]
        table['Health advice'] = callums[i]

    listo.append(table)

final = pd.concat(listo)

print(final)
driver.close()