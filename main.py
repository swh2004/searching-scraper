

from bs4 import BeautifulSoup
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

def fetch_image_and_filter_logos(lst):
    for url in lst:
      response = requests.get(url)

      soup = BeautifulSoup(response.text, 'html.parser')

      images = soup.find_all('img')
      image_url_lst = []
      for image in images:
        image_url = image['src']
        image_url_lst.append(image_url)
      
        
        print(image_url)
# Function to run scraping
def run_scrape(source, query, start_page, pages, limits, username, password):
    
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
      auth=(username, password),#Oxylabs to get tokens
      json=payload,
    )

    if response.status_code != 200:
      print("Error - ", response.json())
      exit(-1)

    #pprint(response.json())

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
        e=pure_Data[1]
        f=e.split('\'')
        for fs in f:
            if 'http' in fs:
                pure.append(fs)

      
    #print(pure)
    my_df = pd.DataFrame(pure)
    my_df.to_csv('links.csv', index=False, header=False)



source = sheet['B1'].value 
query =  sheet['B2'].value 
start_page = int(sheet['B3'].value)
pages = int(sheet['B4'].value)
limits = int(sheet['B5'].value)
username = sheet['B6'].value
password = sheet['B7'].value



run_scrape(source, query, start_page, pages, limits, username, password)

# Open the CSV file 
wb2 = openpyxl.load_workbook('links.csv')
sheet2 = wb2['Sheet1'] 


        

