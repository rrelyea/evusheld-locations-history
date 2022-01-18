import pprint
import os
from re import search
import pandas as pd

from googleapiclient.discovery import build

def searchAndSave(filename, site):
  if site == "":
    return

  totalResults = 1
  startNum = 1
  items = None
  while totalResults >= startNum and startNum <= 100:
    searchResult = service.cse().list(
      q='evusheld',
      cx='37cfbc896668324c4',
      siteSearch=site,
      start=startNum
      ).execute()
 
    totalResults = int(searchResult['searchInformation']['totalResults'])
    pprint.pprint(filename + " " + str(startNum) + " " + str(totalResults))
    if totalResults == 0: 
      items = "[]"
    elif items == None:
      items = searchResult['items']
    else:
      items.extend(searchResult['items'])

    startNum = startNum + 10

  f=open(targetPath + filename + '.json', 'w+', encoding='utf8')

  pprint.pprint(items, stream=f)
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
