import csv
import json
import requests
from bs4 import BeautifulSoup

url = 'https://www.rabota.md/search/?query=python&searchType=1&cityID=1'

page = requests.get(url, stream=True)
soup = BeautifulSoup(page.content, 'html.parser')

data = []
jobs = soup.find_all('div', {'class': 'preview'})
for job in jobs:
    h3 = job.find('h3')
    company_data = job.find('div')
    if h3 and company_data:
        title = h3.find('a', class_='vacancy').text
        company_data = job.find('div').text.replace('\n', '').split('•')
        company = company_data[0].strip()
        location = company_data[1].strip()
        description = job.find('p').text.replace('\n', ' ').strip()
        date_added = job.find_all('span')[-2].text
        salary = job.find_all('span')[-1].text.replace('\n', '').strip()
        data.append({
            'title': title, 'company': company,
            'location': location, 'description': description,
            'date_added': date_added, 'salary': salary
        })
        

with open('data.csv', 'w', newline='', encoding='utf-8') as csv_file:
    keys = data[0].keys()
    dict_writer = csv.DictWriter(csv_file, fieldnames=keys)
    dict_writer.writeheader()
    dict_writer.writerows(data)


with open('data.json', 'w') as json_file:
    json.dump(data, json_file)
    