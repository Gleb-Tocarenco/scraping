import csv
import json
import requests
from bs4 import BeautifulSoup

schema = 'https://www.rabota.md/search/'
href = '?query=python&searchType=1&cityID=1'
pages = [schema + href]

while True:
    page = requests.get(schema + href)
    soup = BeautifulSoup(page.content, 'html.parser')
    pagination = soup.find('div', class_='pagination')
    active = pagination.find('a', class_='active')
    next_sibilings = active.find_next_siblings()
    
    if not next_sibilings:
        break
    next_page = active.find_next_siblings()[0]
    href = next_page['href']
    pages.append(schema + href)

print(pages)