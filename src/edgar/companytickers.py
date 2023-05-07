import requests

headers = {'User-Agent': 'varuntheja.atp@gmail.com'}
companyTickers = requests.get('https://www.sec.gov/files/company_tickers.json', headers=headers)
print(companyTickers.json())

