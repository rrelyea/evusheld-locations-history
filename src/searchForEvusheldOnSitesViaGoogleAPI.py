import pprint
import os
from re import search
import pandas as pd
import json

from googleapiclient.discovery import build

def searchAndSave(filename, site):
  if site == "":
    return

  searchResult = service.cse().list(
      q='evusheld',
      cx='37cfbc896668324c4',
      siteSearch=site
      ).execute()
 
  if searchResult['searchInformation']['totalResults'] == '0': 
    pprint.pprint('no search results for ' + filename)

  searchInfo = searchResult['searchInformation']
  # remove properties that will cause changes to be detected in file, even if search results are identical.
  del searchInfo['searchTime']
  del searchInfo['formattedSearchTime']
  del searchInfo['formattedTotalResults']
  f=open(targetPath + filename + '.json', 'w+', encoding='utf8')

  pprint.pprint(searchResult, stream=f)
  f.close()

# Loop through all states/territories
#   do search of their site and their health site
#   save results to a json file
states = pd.read_csv('state-health-departments.csv')
targetPath = './data/stateSearches/'
while not os.path.exists(targetPath):
  os.mkdir(targetPath)
key = open("key.txt", "r").readlines()
service = build("customsearch", "v1",
          developerKey=key)

for idx, row in states.iterrows():
  state_code = row[3].strip()
  healthDept_site = row[0].strip()
  state_site = row[1].strip()

  if state_code != "":
    searchAndSave(state_code, state_site)
    searchAndSave(state_code + "-Health", healthDept_site)
