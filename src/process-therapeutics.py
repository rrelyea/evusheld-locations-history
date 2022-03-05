from fileinput import filename
import json
from io import StringIO
import os
from os.path import exists
import requests
from urllib.parse import urlparse
import csv

with open("../../therapeutics-archive.json", "r") as read_file:
    publishings = json.load(read_file)
    urls = []

    for publishing in publishings:
      urls.append(publishing["archive_link"]["url"])

# download all new files
for url in sorted(urls):
  filename = os.path.basename(urlparse(url).path)
  localFile = 'archive/'+filename
  if not exists(localFile):
    r = requests.get(url, allow_redirects=True)
    open(localFile, 'wb').write(r.content)

zipSet = set()
url = sorted(urls)[len(urls) - 1]
filename = os.path.basename(urlparse(url).path)
localFile = 'archive/'+filename
with open(localFile, 'r',encoding='utf8') as data:
  reader = csv.reader(data)
  for columns in reader:
    zip = columns[6]
    if zip != "Zip" and 'Evusheld' == columns[8]:
      zipSet.add(zip[0:5])

print(str(len(zipSet)) + ' zipcodes:')
for zipCode in sorted(zipSet):
  print(zipCode, end=', ', flush=True)

  with open(str(zipCode)+'.csv', "w") as f:
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