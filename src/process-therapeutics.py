from fileinput import filename
import json
from io import StringIO
import os
import sys
from os.path import exists
import requests
from urllib.parse import urlparse
import csv

# locally, when I test, I need to pass "../../" as argv[1]
localBasePath = sys.argv[1] if len(sys.argv) > 1 else ""

with open(localBasePath + "data/therapeutics-last-processed.txt", "r") as lastProcessed_file:
  lastProcessedDate = lastProcessed_file.readline()
  print("last processed: " + lastProcessedDate)

newLastProcessDate = None
with open(localBasePath + "data/therapeutics-archive.json", "r") as read_file:
    publishings = json.load(read_file)
    urls = []

    for publishing in publishings:
      updateDate = publishing["update_date"]
      if updateDate > lastProcessedDate:
        urls.append(publishing["archive_link"]["url"])
        newLastProcessDate = updateDate

# download all new files
for url in sorted(urls):
  filename = os.path.basename(urlparse(url).path)
  localFile = localBasePath + 'data/therapeutics/' + filename
  if not exists(localFile):
    r = requests.get(url, allow_redirects=True)
    open(localFile, 'wb').write(r.content)

if len(urls) > 0:
    # calculate all zip codes, by looking at latest data file
    # note - if a provider was listed earlier, but isn't in the latest data file, their zip code might not be processed
    #      - tracking this problem here: https://github.com/rrelyea/evusheld-locations-history/issues/11
    zipSet = set()
    url = sorted(urls)[len(urls) - 1]
    filename = os.path.basename(urlparse(url).path)
    localFile = localBasePath + 'data/therapeutics/'+filename
    with open(localFile, 'r',encoding='utf8') as data:
      reader = csv.reader(data)
      for columns in reader:
        zip = columns[6]
        if zip != "Zip" and 'Evusheld' == columns[8]:
          zipSet.add(zip[0:5])

    print(str(len(zipSet)) + ' zipcodes:')
    for zipCode in sorted(zipSet):
      print(zipCode, end=', ', flush=True)

      with open(localBasePath + 'data/dose-details/'+str(zipCode)+'.csv', "a") as f:
        for url in sorted(urls):
          filename = os.path.basename(urlparse(url).path)
          localFile = 'archive/'+filename
          timeStamp = filename.replace('rxn6-qnx8_','').replace('.csv','')
          with open(localFile, 'r',encoding='utf8') as data:
            reader = csv.reader(data)
            for columns in reader:
              zip = columns[6]
              provider = columns[0]
              if "," in provider:
                provider = '"' + provider + '"'
              if zip[0:5] == zipCode and 'Evusheld' == columns[8]:
                f.write(timeStamp + ',' + zip + ',' + provider)
                for i in range(9, 14):
                  if i < len(columns):
                    f.write(',' + columns[i])
                  else:
                    f.write(',')
                f.write('\n')
        f.close()

    with open("../../data/therapeutics-last-processed.txt", "w") as lastProcessed_file:
      lastProcessedDate = lastProcessed_file.write(newLastProcessDate)