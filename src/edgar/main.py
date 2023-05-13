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

interested_forms = allForms[allForms.apply(lambda x: x['form'] in ["10-K", ], axis=1)] # "10-Q", "DEF 14A", "8-K"

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

# text_file_locations = get_textfile_locations(cik_stripped=cik_stripped, df=quarter_end_filings)

def primaryDocumentLocation(cik_stripped, row, prefix='https://www.sec.gov/Archives/edgar/data/'):
    """
    given the row of dataframe
    find the location of the primary document
    """
    location = prefix + cik_stripped + '/' + row['accessionNumber'].replace('-', '') + '/' + row['primaryDocument']
    return location

for index, row in interested_forms.iterrows():
    response = requests.get(primaryDocumentLocation(cik_stripped, row), headers=headers)
    if response.status_code == 200:
        with open("./data/" + row['primaryDocument'], 'wb') as f:
            f.write(response.content)

