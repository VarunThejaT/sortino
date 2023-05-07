import json 
import pandas as pd
import requests

cik = "0001326801" # meta
# cik = "0000320193" # apple
headers = {'User-Agent': 'varuntheja.atp@gmail.com'}
filingMetadata = requests.get(f'https://data.sec.gov/submissions/CIK{cik}.json',headers=headers)
companyFacts = requests.get(f'https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json', headers=headers)

x = companyFacts.json()

# dictionary to dataframe
allForms = pd.DataFrame.from_dict(
             filingMetadata.json()['filings']['recent']
             )
cik_stripped = cik.lstrip("0")

quarter_end_filings = allForms[allForms.apply(lambda x: x['form'] in ["10-Q", "10-K", "10 K", "10 Q"], axis=1)]
quarter_end_filings

def get_textfile_locations(cik_stripped, df):
    """
    given the df containing 10-K and 10-Q filings 
    extract the location of the txt formatted filings
    to be downloaded
    """
    rv = []
    for index, row in df.iterrows():
        print(row)
        location = 'https://www.sec.gov/Archives/edgar/data/' + cik_stripped + '/' + row['accessionNumber'].replace('-', '') + '/' + row['accessionNumber'] + '.txt'
        rv.append(location)
        print(location)
    return rv

text_file_locations = get_textfile_locations(cik_stripped=cik_stripped, df=quarter_end_filings)

# response = requests.get('https://www.sec.gov/Archives/edgar/data/1326801/000132680123000067/0001326801-23-000067.txt', headers=headers)
# if response.status_code == 200:
#     with open('test_data.txt', 'wb') as f:
#         f.write(response.content)

