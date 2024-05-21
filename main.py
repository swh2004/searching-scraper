pip install requests 
import pandas as pd

import openpyxl
import time
import requests
import pandas as pd
import requests
from pprint import pprint
import csv

# Open the Excel file 
wb = openpyxl.load_workbook('data.xlsx')
sheet = wb['Sheet1'] 

# Function to run scraping
def run_scrape(source, query, start_page, pages, limits):
    
    payload = {
      'source': source,
      'query': query,
      'parse': True,
      'start_page': start_page,
      'pages': pages,
      'limit': limits,
    }

    response = requests.request(
      'POST',
      'https://realtime.oxylabs.io/v1/queries',
      auth=('baigao_ouo', 'Qyj757604swh'),
      json=payload,
    )

    if response.status_code != 200:
      print("Error - ", response.json())
      exit(-1)

    pprint(response.json())

    data = response.json()
    mystr=str(data['results'])
    datas=mystr.split(',')

    dds=[]
    for d in datas:
      if '\'url\':' in d:
        if 'google' not in d:
          dds.append(d)
        
    pure=[]
    for d in dds:
        pure_Data = d.split(':',1)
        pure.append(pure_Data[1])

      
    print(pure)
    my_df = pd.DataFrame(pure)
    my_df.to_csv('my_csv_related.csv', index=False, header=False)
    #pprint(data)
    #df = pd.json_normalize(data['results'])
    #print(df)

    #df.to_csv('export.csv', index=False)

while True:
    
    # Get search term and results from cells
    source = sheet['B1'].value 
    query =  sheet['B2'].value 
    start_page = int(sheet['B3'].value)
    pages = int(sheet['B4'].value)
    limits = int(sheet['B5'].value)
    
    
    # Check for change in modification time
    if wb.monotonic_time != wb._last_saved_monotonic_time:
        
        # Run scraping with new values
        run_scrape(source, query, start_page, pages, limits)
        
        # Update modification time
        wb._last_saved_monotonic_time = wb.monotonic_time
        
    # Sleep and continue checking
    time.sleep(5)
