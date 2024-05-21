import requests
from bs4 import BeautifulSoup

url = "https://www.colvaservices.com/intro-life-settlements/"
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

images = soup.find_all('img')

for image in images:
  image_url = image['src']
  
  print(image_url)
